import os
import time
import zipfile
import subprocess

# List of problem names to process
problem_names = [
      "Two-Sum", "Add-Two-Numbers", "Longest-Substring-Without-Repeating-Characters", 
    "Median-of-Two-Sorted-Arrays", "Longest-Palindromic-Substring", "ZigZag-Conversion", 
    "Reverse-Integer", "String-to-Integer-atoi", "Palindrome-Number", "Regular-Expression-Matching", 
    "Container-With-Most-Water", "Integer-to-Roman", "Roman-to-Integer", "Longest-Common-Prefix", 
    "3Sum", "3Sum-Closest", "Letter-Combinations-of-a-Phone-Number", "4Sum", 
    "Remove-Nth-Node-From-End-of-List", "Valid-Parentheses", "Merge-Two-Sorted-Lists", 
    "Generate-Parentheses", "Merge-k-Sorted-Lists", "Swap-Nodes-in-Pairs", "Reverse-Nodes-in-k-Group", 
    "Remove-Duplicates-from-Sorted-Array", "Remove-Element", "find-the-index-of-the-first-occurrence-in-a-string", "Divide-Two-Integers", 
    "Substring-with-Concatenation-of-All-Words", "Next-Permutation", "Longest-Valid-Parentheses", 
    "Search-in-Rotated-Sorted-Array", "Find-First-and-Last-Position-of-Element-in-Sorted-Array", 
    "Search-Insert-Position", "Valid-Sudoku", "Sudoku-Solver", "Count-and-Say", "Combination-Sum", 
    "Combination-Sum-II", "First-Missing-Positive", "Trapping-Rain-Water", "Multiply-Strings", 
    "Wildcard-Matching", "Jump-Game-II", "Permutations", "Permutations-II", "Rotate-Image", 
    "Group-Anagrams", "powx-n", "N-Queens", "N-Queens-II", "Maximum-Subarray", "Spiral-Matrix", 
    "Jump-Game", "Merge-Intervals", "Insert-Interval", "Length-of-Last-Word", "Spiral-Matrix-II", 
    "Permutation-Sequence", "Rotate-List", "Unique-Paths", "Unique-Paths-II", "Minimum-Path-Sum", 
    "Valid-Number", "Plus-One", "Add-Binary", "Text-Justification", "Sqrtx", "Climbing-Stairs", 
    "Simplify-Path", "Edit-Distance", "Set-Matrix-Zeroes", "Search-a-2D-Matrix", "Sort-Colors", 
    "Minimum-Window-Substring", "Combinations", "Subsets", "Word-Search", "Remove-Duplicates-from-Sorted-Array-II", 
    "Search-in-Rotated-Sorted-Array-II", "Remove-Duplicates-from-Sorted-List-II", "Remove-Duplicates-from-Sorted-List", 
    "Largest-Rectangle-in-Histogram", "Maximal-Rectangle", "Partition-List", "Scramble-String", "Merge-Sorted-Array", 
    "Gray-Code", "Subsets-II", "Decode-Ways", "Reverse-Linked-List-II", "Restore-IP-Addresses", 
    "Binary-Tree-Inorder-Traversal", "Unique-Binary-Search-Trees-II", "Unique-Binary-Search-Trees", 
    "Interleaving-String", "Validate-Binary-Search-Tree", "Recover-Binary-Search-Tree","Same-Tree"
]

output_folder = "leetcode_solutions"
os.makedirs(output_folder, exist_ok=True)

# Loop through each problem
for i, problem in enumerate(problem_names):
    print(f"\n🟩 [{i+1}/{len(problem_names)}] Scraping: {problem}")
    os.system(f'python scrape_script.py "{problem}"')
    print(f"✅ Finished: {problem}")
    
    if i != len(problem_names) - 1:
        print("⏳ Waiting 1 minute before next...")
        time.sleep(50)

# Zip the folder
def zip_folder(folder_path, zip_name):
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, folder_path)
            zipf.write(full_path, arcname)
    zipf.close()

zip_folder(output_folder, "leetcode_solutions.zip")
print("\n📦 All solutions zipped as leetcode_solutions.zip")

# Open the folder in Explorer
subprocess.Popen(f'explorer "{os.path.abspath(output_folder)}"')
print("📂 Folder opened!")
