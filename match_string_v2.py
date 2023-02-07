import re
import sys
from difflib import SequenceMatcher

# a = 'I grAmaqlO prajala praधAna wRtti wyawasAyaq'
# b = 'IgrAmaqlOprajalapraधAnawRtti,wyawasAyaq'

# a = 'mUडu budधamatIdEwi wigrahAnni kOटa nuqci kAjEyAli adi uqडagA टrOy gOडalanu mIru paडagoटटalEru ani caqdruडu rUpaधaruडiki ceppAडu'
# b = 'mUडu,mUडubudधamatIdEwiwigrahAnnikOटanuqcinuqciadi,uqडagA,टrOygOडalanumIrupaडagoटटalEru,anicaqdruडu,rUpaधaruडikiceppAडu'

# out = 'mUडu, mUडu budधamatIdEwi wigrahAnni kOटa nuqci nuqci adi, uqडagA,  टrOy gOडalanu mIru paडagoटटalEru, ani caqdruडu, rUpaधaruडiki ceppAडu'

a = 'brahmadattuडu kAशIrAjyAnnI paripAliqcE kAlaqlO A nagaraqlO धanikuडऐna oka goppawartakuडuqडEwAडu Ayanaku mitrawiqdakuडani oka koडukuqडE wAडu I mitrawiqdakuडu eqtO pApAtmuडu wartakuडu canipOyAka Ayana BArya tana kumAruडiki nAyanA dAnAlu ceyyi niyamAlu pAटiqcu धarmaq anusariqcu ani eqtO hitabOधa cEsiqdi kAni wAडu talli mAटalu koqcemऐnA winipiqcukOlEdu'
b = 'brahmadattuडu,kAशIrAjyAnnIparipAliqcEkAlaqlO,AnagaraqlOधanikuडऐna,okagoppawartakuडuqडEwAडu,Ayanaku,mitrawiqdakuडaniokakoडukuqडEwAडu,Imitrawiqdakuडu,eqtOpApAtmuडu,wartakuडucanipOyAka,AyanaBArya,tanakumAruडiki,nAyanA,dAnAlu,dAnAluniyamAlupAटiqcu,pAटiqcuधarmaq,anusariqcu,anieqtOhitabOधacEsiqdi,kAni,wAडu,tallimAटalukoqcemऐnAwinipiqcukOlEdu'

def seq_matcher(a,b,verbose=False):
    s = SequenceMatcher(None, a, b)

    out_str = ''
    error_flag = 0
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if verbose:
            print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))
        if tag != 'equal':
            if a[i1:i2] == ' ':
                if b[j1:j2] == '':
                    out_str = out_str+' '
                elif b[j1:j2] == ',':
                    out_str = out_str+', '
                else:
                    error_flag = 1
            else:
                error_flag = 1
        else:
            out_str = out_str+' '+b[j1:j2]+' '
    
    out_str = re.sub(" ,", ",", out_str)
    out_str = re.sub(",", ", ", out_str)
    out_str = re.sub(" +", " ", out_str)

    if error_flag == 1:
        return 'Error'
    else:
        return out_str.strip()

def non_matching_seq_matcher(a,b,verbose=False):
    s = SequenceMatcher(None, a, b)

    out_str = ''
    error_flag = 0
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if verbose:
            print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))
        if tag == 'equal':
            if len(b[j1:j2]) > 1:
                out_str = out_str+' '+b[j1:j2]+' '
            else:
                out_str = re.sub(" +$", "", out_str)+b[j1:j2]
        elif tag == 'delete':
            if a[i1:i2] == ' ':
                if b[j1:j2] == '':
                    out_str = out_str+' '
                else:
                    error_flag = 1
            else:
                error_flag = 1
        elif tag == 'replace':
            if a[i1:i2] == ' ':
                if b[j1:j2] == ',':
                    out_str = out_str+', '
                else:
                    out_str = out_str+' '+b[j1:j2]+' '
            else:
                out_str = out_str+' '+b[j1:j2]+' '
        elif tag == 'insert':
            if a[i1:i2] == '':
                out_str = out_str+' '+b[j1:j2]+' '
            else:
                error_flag = 1
        else:
            error_flag = 1

    out_str = re.sub(" +,", ",", out_str)
    out_str = re.sub(",", ", ", out_str)
    out_str = re.sub(" +", " ", out_str)

    if error_flag == 1:
        return 'Error'
    else:
        return out_str.strip()

def main(phone_file, HS_file, out_file,verbose=False):
    # phone_file = 'text_phone'
    # HS_file = 'text_HS'
    with open(phone_file) as fid1, open(HS_file) as fid2:
        file1_lines = fid1.read().strip().split('\n')
        file2_lines = fid2.read().strip().split('\n')
    
    out_data = []
    id_mismatch_lines = 0
    str_mismatch_lines = 0

    if len(file1_lines) == len(file2_lines):
        for i in range(0,len(file1_lines)):
            phone_line = file1_lines[i].strip().split(" ", 1)
            HS_line = file2_lines[i].strip().split(" ", 1)
            if phone_line[0] == HS_line[0]:
                if verbose:
                    print(f"Line ID: {phone_line[0]}")
                out_line = seq_matcher(phone_line[1].strip(),HS_line[1].strip())
                if out_line == 'Error':
                    new_out_line = non_matching_seq_matcher(phone_line[1].strip(),HS_line[1].strip())
                    if new_out_line == 'Error':
                        print(f"Error! String Mismatch. Line ID (phone:{phone_line[0]}, HS:{HS_line[0]})! Line number: {str(i)}")
                        str_mismatch_lines += 1
                    else:
                        out_data.append(phone_line[0]+' '+new_out_line)
                else:
                    out_data.append(phone_line[0]+' '+out_line)
            else:
                print(f"Error! Line IDs (phone:{phone_line[0]}, HS:{HS_line[0]}) doesn't match! Line number: {str(i)}")
                id_mismatch_lines += 1
    else:
        sys.exit("Number of lines in both files doesn't match.")
    
    print(f"Number of lines with string mismatch: {str_mismatch_lines}\nNumber of lines with id mismatch: {id_mismatch_lines}")

    if out_data:
        with open(out_file,'w') as fid:
            fid.write("\n".join(out_data))
    
    print(f"Number of lines in input: {len(file1_lines)}\nNumber of lines in output: {len(out_data)}\nNumber of error lines: {id_mismatch_lines+str_mismatch_lines}")

if __name__=="__main__":
    # a = 'I grAmaqlO prajala praधAna wRtti wyawasAyaq'
    # b = 'IgrAmaqlOprajalapraधAnawRtti,wyawasAyaq'
    # seq_matcher(a,b)
    phone_file = 'text_phone'
    HS_file = 'text_HS'
    out_file = 'out_phone_new'
    main(phone_file, HS_file, out_file)