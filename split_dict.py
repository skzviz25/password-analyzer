# split_dict.py
def split_file(filename, lines_per_file=500000):
    with open(filename, 'r', encoding='latin-1') as f:
        count = 0
        file_num = 1
        current_out_file = open(f'rockyou_part_{file_num}.txt', 'w', encoding='latin-1')
        
        for line in f:
            current_out_file.write(line)
            count += 1
            if count >= lines_per_file:
                current_out_file.close()
                print(f"Created rockyou_part_{file_num}.txt")
                file_num += 1
                current_out_file = open(f'rockyou_part_{file_num}.txt', 'w', encoding='latin-1')
                count = 0
        current_out_file.close()

if __name__ == "__main__":
    split_file('rockyou.txt')