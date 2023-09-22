def read_file(filename):
    with open(filename, 'r') as file:
        content = file.readlines()
    return content


def is_digit(character):
    return character in '0123456789'


def is_alpha(character):
    return 'a' <= character <= 'z' or 'A' <= character <= 'Z'


def is_valid_email_character(character):
    return is_alpha(character) or is_digit(character) or character in ['.', '-', '_']


def find_emails(line):
    emails = []
    i = 0
    while i < len(line):
        if is_valid_email_character(line[i]):
            start = i
            while i < len(line) and line[i] != '@':
                i += 1
            if i < len(line) and line[i] == '@':
                i += 1
                while i < len(line) and line[i] != '.':
                    i += 1
                if i < len(line) and line[i] == '.':
                    end = i
                    while i < len(line) and is_valid_email_character(line[i]):
                        i += 1
                    emails.append(line[start:i])
        i += 1
    return emails


def find_phone_numbers(line):
    phone_numbers = []
    i = 0
    while i < len(line):
        if is_digit(line[i]):
            start = i
            count_digits = 0
            while i < len(line) and (is_digit(line[i]) or line[i] in ['-', ' ', '(', ')']):
                if is_digit(line[i]):
                    count_digits += 1
                i += 1
            if count_digits == 10:
                phone_numbers.append(line[start:i])
        i += 1
    return phone_numbers


def extract_information_from_file(filename):
    lines = read_file(filename)
    all_emails = []
    all_phone_numbers = []
    for line in lines:
        emails = find_emails(line)
        phone_numbers = find_phone_numbers(line)
        all_emails.extend(emails)
        all_phone_numbers.extend(phone_numbers)
    return all_emails, all_phone_numbers


def write_to_file(filename, emails, phone_numbers):
    with open(filename, 'w') as file:
        file.write("Emails:\n")
        for email in emails:
            file.write(email + "\n")
        file.write("\nPhone Numbers:\n")
        for phone_number in phone_numbers:
            file.write(phone_number + "\n")


def main():
    input_filename = "sample.txt"
    output_filename = "output.txt"
    emails, phone_numbers = extract_information_from_file(input_filename)
    write_to_file(output_filename, emails, phone_numbers)


if __name__ == "__main__":
    main()
