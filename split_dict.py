import os

def split_file_safely(filename, lines_per_file=500000):
    # Ensure the original file exists
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return

    with open(filename, 'r', encoding='latin-1') as f:
        file_num = 1
        line_count = 0
        
        # Open the first part
        current_out_file = open(f'rockyou_part_{file_num}.txt', 'w', encoding='latin-1')
        
        for line in f:
            # strip and re-add newline to ensure consistency
            clean_line = line.strip()
            if clean_line:
                current_out_file.write(clean_line + "\n")
                line_count += 1
            
            # Switch to next file if limit reached
            if line_count >= lines_per_file:
                current_out_file.close()
                print(f"Finished rockyou_part_{file_num}.txt")
                file_num += 1
                current_out_file = open(f'rockyou_part_{file_num}.txt', 'w', encoding='latin-1')
                line_count = 0
        
        current_out_file.close()
        print("Splitting complete!")

if __name__ == "__main__":
    split_file_safely('rockyou.txt')