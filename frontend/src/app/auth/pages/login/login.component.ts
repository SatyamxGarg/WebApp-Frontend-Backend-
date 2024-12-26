import { AuthService } from './../../../services/auth.service';
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { Router, RouterModule } from '@angular/router';
import { AuthEndpointsService } from '../../../../swagger/api/services';
import { UserLogin } from '../../../../swagger/api/models/user-login';
import { ResponseWrapperToken } from '../../../../swagger/api/models';
import { finalize } from 'rxjs/operators';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { DropdownModule } from 'primeng/dropdown';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, RouterModule, InputTextModule, PasswordModule, DropdownModule, ButtonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  loader = false;
  loginForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', Validators.required),
    remember: new FormControl(false),
  });

  constructor(
    private authEndpointsService: AuthEndpointsService,
    private authService: AuthService,
    private toastr: ToastrService,
    private router: Router
  ) {}

  onSubmit() {
    if (this.loginForm.invalid) {
      // Mark all fields as touched to trigger validation messages
      Object.keys(this.loginForm.controls).forEach(field => {
        const control = this.loginForm.get(field);
        control?.markAsTouched({ onlySelf: true });
        control?.markAsDirty({ onlySelf: true });
      });
      return;
    }

    this.loader = true;
    const data: UserLogin = {
      email: this.loginForm.get('email')?.value as string,
      password: this.loginForm.get('password')?.value as string,
    };

    this.authEndpointsService
      .loginApiV1AuthLoginPost({ body: data })
      .pipe(finalize(() => (this.loader = false)))
      .subscribe((response: ResponseWrapperToken) => {
        if (response.data?.access_token) {
          this.authService.setAccessToken(response.data.access_token);
          this.toastr.success('Login Successful');
          this.router.navigate(['/home']);
        } else {
          this.toastr.error('Login failed. Please try again.');
        }
      });
  }
}
