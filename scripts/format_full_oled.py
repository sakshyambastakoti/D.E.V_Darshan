import textwrap
import re

def process_file():
    with open("d:/D.E.V_Darshan/full_exam_solutions.txt", "r", encoding="utf-8") as f:
        content = f.read()

    # Split by Questions using regex matching QUESTION N
    question_blocks = re.split(r'(QUESTION \d+ \(.*?\))', content)
    
    output_lines = []

    # First block is preamble / headers
    preamble = question_blocks[0]
    for line in preamble.split('\n'):
        stripped = line.strip()
        if not stripped:
            output_lines.append("")
        elif set(stripped) == {'='} or set(stripped) == {'-'}:
            output_lines.append(stripped[0] * 32)
        else:
            wrapped = textwrap.wrap(line, width=32, break_long_words=True, break_on_hyphens=False)
            output_lines.extend(wrapped)

    # Process Question blocks in pairs: (Header, Body)
    for i in range(1, len(question_blocks), 2):
        q_header = question_blocks[i].strip()  # e.g., "QUESTION 10 (2 Marks - Numerical)"
        q_body = question_blocks[i+1] if (i+1) < len(question_blocks) else ""

        # Extract question number
        q_num_match = re.search(r'QUESTION (\d+)', q_header)
        q_num = q_num_match.group(1) if q_num_match else str(i)

        # Clear Start Marker for OLED
        output_lines.append("")
        output_lines.append("=" * 32)
        
        # Wrap q_header if > 32 chars
        header_sublines = textwrap.wrap(q_header, width=32, break_long_words=True, break_on_hyphens=False)
        for h_sub in header_sublines:
            output_lines.append(h_sub.center(32))
            
        output_lines.append("=" * 32)
        output_lines.append("")

        # Process q_body lines
        body_lines = q_body.split('\n')
        for b_line in body_lines:
            stripped = b_line.strip()
            if set(stripped) == {'='} or set(stripped) == {'-'}:
                output_lines.append("-" * 32)
            elif not stripped:
                output_lines.append("")
            else:
                indent_len = len(b_line) - len(b_line.lstrip())
                indent_str = " " * min(indent_len, 4)
                
                wrapped = textwrap.wrap(
                    b_line.strip(),
                    width=32 - len(indent_str),
                    break_long_words=True,
                    break_on_hyphens=False
                )
                for w in wrapped:
                    output_lines.append(indent_str + w)

        # Clear End Marker for OLED
        end_marker = f"[ END OF QUESTION {q_num} ]"
        output_lines.append("")
        output_lines.append("-" * 32)
        output_lines.append(end_marker.center(32))
        output_lines.append("-" * 32)
        output_lines.append("")

    # Join output text
    full_text = '\n'.join(output_lines)
    
    # Strictly collapse multiple blank lines down to max 1 line gap (\n\n)
    single_gap_text = re.sub(r'\n{3,}', '\n\n', full_text)
    final_lines = single_gap_text.split('\n')

    # Verify line lengths
    errors = 0
    for idx, l in enumerate(final_lines, 1):
        if len(l) > 32:
            print(f"Error line {idx}: len={len(l)}: '{l}'")
            errors += 1
            
    print(f"Total output lines: {len(final_lines)}")
    print(f"Max line length: {max(len(l) for l in final_lines)}")
    print(f"Errors (>32 chars): {errors}")

    if errors == 0:
        with open("d:/D.E.V_Darshan/full_exam_solutions_oled.txt", "w", encoding="utf-8") as f:
            f.write(single_gap_text.strip() + '\n')
        print("Successfully written to full_exam_solutions_oled.txt with single line gap!")

if __name__ == "__main__":
    process_file()
