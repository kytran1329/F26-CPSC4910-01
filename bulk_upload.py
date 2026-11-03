
def validate_bulk_upload(file, user_role):
    valid_records = []
    errors = []

    # Check that a file was provided
    if file is None:
        return [], ["No file was provided."]

    # Validate user role
    if user_role not in ("Admin", "Sponsor"):
        return [], ["Unauthorized upload role."]

    # Read and process each line
    try:
        for line_number, line in enumerate(file, start=1):

            # Decode uploaded file
            try:
                if isinstance(line, bytes):
                    line = line.decode("utf-8-sig")
                elif not isinstance(line, str):
                    errors.append(
                        f"Line {line_number}: Invalid line format."
                    )
                    continue

            except UnicodeDecodeError:
                errors.append(
                    f"Line {line_number}: Invalid UTF-8 encoding."
                )
                continue

            # Remove surrounding whitespace
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Reject unexpected binary characters
            if "\x00" in line:
                errors.append(
                    f"Line {line_number}: File contains invalid binary characters."
                )
                continue

            # Split the line using the pipe delimiter
            fields = line.split("|")

            # Remove surrounding whitespace from fields
            fields = [field.strip() for field in fields]

            # Validate record type
            record_type = fields[0]

            if record_type not in ("O", "D", "S"):
                errors.append(
                    f"Line {line_number}: Invalid record type '{record_type}'."
                )
                continue

            # Validate number of fields
            if record_type == "O":
                if len(fields) != 2:
                    errors.append(
                        f"Line {line_number}: Organization records must have 2 fields."
                    )
                    continue

            elif record_type in ("D", "S"):
                if len(fields) < 5 or len(fields) > 7:
                    errors.append(
                        f"Line {line_number}: Driver and Sponsor records "
                        f"must have between 5 and 7 fields."
                    )
                    continue

            # Assign field values
            organization = fields[1]

            if record_type == "O":
                first_name = ""
                last_name = ""
                email = ""
                points = ""
                reason = ""

            else:
                first_name = fields[2]
                last_name = fields[3]
                email = fields[4]

                points = fields[5] if len(fields) >= 6 else ""
                reason = fields[6] if len(fields) == 7 else ""

            # Validate user permissions
            if user_role == "Sponsor" and record_type == "O":
                errors.append(
                    f"Line {line_number}: Sponsors cannot create organizations."
                )
                continue

            # Sponsors must leave organization blank
            if user_role == "Sponsor" and organization:
                errors.append(
                    f"Line {line_number}: Sponsors must leave organization blank."
                )
                continue

            # Validate organization records
            if record_type == "O":

                if not organization:
                    errors.append(
                        f"Line {line_number}: Organization name is required."
                    )
                    continue

                valid_records.append({
                    "type": "O",
                    "organization": organization,
                    "line_number": line_number
                })

                continue

            # Validate driver and sponsor information
            if not first_name or not last_name or not email:
                errors.append(
                    f"Line {line_number}: First name, last name, "
                    "and email are required."
                )
                continue

            # Sponsors cannot receive points
            if record_type == "S" and (points or reason):
                errors.append(
                    f"Line {line_number}: Points cannot be assigned to sponsors."
                )
                continue

            # Validate points and reason
            if points:

                try:
                    points = float(points)

                except ValueError:
                    errors.append(
                        f"Line {line_number}: Points must be a valid number."
                    )
                    continue

                if not reason:
                    errors.append(
                        f"Line {line_number}: A reason is required "
                        "when points are provided."
                    )
                    continue

            else:
                points = None

                if reason:
                    errors.append(
                        f"Line {line_number}: A reason cannot be "
                        "provided without points."
                    )
                    continue

            # Save valid record
            valid_records.append({
                "type": record_type,
                "organization": organization,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "points": points,
                "reason": reason if points is not None else None,
                "line_number": line_number
            })

    except Exception as e:
        errors.append(
            f"Unable to read uploaded file: {str(e)}"
        )

    return valid_records, errors
