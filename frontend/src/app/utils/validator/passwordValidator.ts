import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

// Custom password validator function
export function passwordValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const value = control.value;

    if (!value) return null; // If the field is empty, don't validate yet

    const errors: { [key: string]: boolean } = {};
    const hasUpperCase = /[A-Z]/.test(value);
    const hasLowerCase = /[a-z]/.test(value);
    const hasNumbers = /\d/.test(value);
    const hasSpecialChars = /[!@#$%^&*(),.?":{}|<>]/.test(value);
    const isValidLength = value.length >= 8;

    if (!hasUpperCase) {
      errors['missingUpperCase'] = true;
    }
    if (!hasLowerCase) {
      errors['missingLowerCase'] = true;
    }
    if (!hasNumbers) {
      errors['missingNumber'] = true;
    }
    if (!hasSpecialChars) {
      errors['missingSpecialChar'] = true;
    }
    if (!isValidLength) {
      errors['invalidLength'] = true;
    }

    return Object.keys(errors).length ? errors : null; // Return the errors object if there are any errors
  };
}
