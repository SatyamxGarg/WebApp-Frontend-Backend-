import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AuthEndpointsService } from '../../../../swagger/api/services';
import { UserSignUp } from '../../../../swagger/api/models/user-sign-up';
import { ResponseWrapperToken, Token } from '../../../../swagger/api/models';
import { AuthService } from '../../../services/auth.service';
import { passwordValidator } from '../../../utils/validator/passwordValidator';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext'; 

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterModule, PasswordModule, ButtonModule, ],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.scss',
})
export class SignupComponent {
  private authEndpointsService: AuthEndpointsService = inject(AuthEndpointsService);
  private authService: AuthService = inject(AuthService);

  firstName = new FormControl('', [Validators.required]);
  lastName = new FormControl('', [Validators.required]);
  email = new FormControl('', [Validators.required, Validators.email]);
  password = new FormControl('', [Validators.required, passwordValidator()]);
  cpassword = new FormControl('', [Validators.required]);
  loader: boolean = false;

  signUp = new FormGroup({
    firstName: this.firstName,
    lastName: this.lastName,
    email: this.email,
    password: this.password,
    cpassword: this.cpassword,
  });

  constructor(
    private toastr: ToastrService,
    private route: Router
  ) {}

  onSubmit() {
    if (this.signUp.valid && this.signUp.value.password == this.signUp.value.cpassword) {
      this.loader = true;
      const data: UserSignUp = {
        email: this.signUp.value.email as string,
        password: this.signUp.value.password as string,
        first_name: this.signUp.value.firstName as string,
        last_name: this.signUp.value.firstName as string,
      };
      this.authEndpointsService
        .signupApiV1AuthSignupPost({ body: data })
        .subscribe((response: ResponseWrapperToken) => {
          this.authService.setAccessToken(response.data?.access_token);
          this.toastr.success('Registration Succsessful');
          this.loader = false;
          this.route.navigate(['/home']);
        });
    } else {
      Object.keys(this.signUp.controls).forEach(field => {
        const control = this.signUp.get(field);
        control?.markAsTouched({ onlySelf: true });
        control?.markAsDirty({ onlySelf: true });
      });
    }
  }
}
