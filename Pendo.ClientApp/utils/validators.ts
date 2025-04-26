/**
 * Validates and sets a cost value with two-decimal precision within given bounds.
 *
 * @param setCost - Setter function for the cost state.
 * @param input - Raw input string to validate.
 * @param min - Minimum allowed cost (inclusive).
 * @param max - Maximum allowed cost (inclusive).
 * @param setValidationMessage - Optional setter for validation error messages.
 */
export const costValidator = (
    setCost: (value: string) => void,
    input: string,
    min: number,
    max: number,
    setValidationMessage: ((msg: string | null) => void) | null = null
): void => {
    if (setValidationMessage) {
        setValidationMessage(null);
    }

    if (input === '') {
        setCost('');
        return;
    }

    const regex = /^\d*\.?\d{0,2}$/;
    if (!regex.test(input)) {
        return;
    }

    const asFloat = parseFloat(input);
    if (!isNaN(asFloat) && asFloat >= min && asFloat <= max) {
        setCost(input);
    } else if (isNaN(asFloat)) {
        setCost(input);
    } else if (setValidationMessage) {
        setValidationMessage(`Cost must be between £${min} and £${max}`);
    }
};

/**
 * Validates and sets an integer value within given bounds.
 *
 * @param setValue - Setter function for the integer state.
 * @param input - Raw input string to validate.
 * @param min - Minimum allowed integer (inclusive).
 * @param max - Maximum allowed integer (inclusive).
 * @param setValidationMessage - Optional setter for validation error messages.
 */
export const integerValidator = (
    setValue: (value: string) => void,
    input: string,
    min: number | null,
    max: number,
    setValidationMessage: ((msg: string | null) => void) | null = null
): void => {
    if (setValidationMessage) {
        setValidationMessage(null);
    }

    if (input === '') {
        setValue('');
        return;
    }
    
    const regex = /^\d*$/;
    if (!regex.test(input)) {
        return;
    }

    const asInt = parseInt(input, 10);
    if (!isNaN(asInt) && (min === null || asInt >= min) && asInt <= max) {
        setValue(input);
    } else if (isNaN(asInt)) {
        setValue(input);
    } else if (setValidationMessage) {
        if (min !== null) {
            setValidationMessage(`Value must be between ${min} and ${max}`);
        }
        else {
            setValidationMessage(`Value must be between 0 and ${max}`);
        }
    }
};

/**
 * Validates and sets a string value based on allowed length bounds.
 *
 * @param setValue              - Setter function for the string state.
 * @param input                 - Raw input string to validate.
 * @param min                   - Minimum allowed length (inclusive). If `null`, no lower bound is enforced.
 * @param max                   - Maximum allowed length (inclusive).
 * @param setValidationMessage  - Optional setter for validation error messages.
 */
export const stringLengthValidator = (
    setValue: (value: string) => void,
    input: string,
    min: number | null,
    max: number,
    setValidationMessage: ((msg: string | null) => void) | null = null
): void => {
    // clear any previous validation error
    if (setValidationMessage) {
        setValidationMessage(null);
    }

    // always allow clearing the field
    if (input === '') {
        setValue('');
        return;
    }

    const length = input.length;
    const lower = min ?? 0;

    // if within bounds, accept the input
    if (length >= lower && length <= max) {
        setValue(input);
    }
    // otherwise, emit an error message (if provided)
    else if (setValidationMessage) {
        if (min !== null) {
            setValidationMessage(`Value must be between ${min} and ${max} characters`);
        } else {
            setValidationMessage(`Value must be no more than ${max} characters`);
        }
    }
};