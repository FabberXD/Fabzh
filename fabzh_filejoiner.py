import io

def merge_files(original_file, modified_file1, modified_file2):
    with io.open(original_file, mode="r", encoding="utf-8") as org_file, \
         io.open(modified_file1, mode="r", encoding="utf-8") as mod_file1, \
         io.open(modified_file2, mode="r", encoding="utf-8") as mod_file2:
        org_lines = org_file.readlines()
        mod1_lines = mod_file1.readlines()
        mod2_lines = mod_file2.readlines()
        if len(org_lines) < len(mod1_lines):
            if len(mod1_lines) < len(mod2_lines):
                addlines = len(mod2_lines) - len(org_lines)
            else:
                addlines = len(mod1_lines) - len(org_lines)
            org_lines[-1] = org_lines[-1]+'\n'
            for i in range(addlines):
                org_lines.append("\n")
            org_lines[-1] = org_lines[-1][:-1]
            print(org_lines)
        output = ""
        for i, org_line in enumerate(org_lines):
            if i < len(mod1_lines) and i < len(mod2_lines):
                output += mod2_lines[i] if mod1_lines[i] == org_line else mod1_lines[i].replace("\n", "")+'\n'
            elif i < len(mod1_lines):
                output += mod1_lines[i]
            elif i < len(mod2_lines):
                output += mod2_lines[i]
        return output