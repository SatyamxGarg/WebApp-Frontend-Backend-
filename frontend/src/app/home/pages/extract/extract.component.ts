import { Component } from '@angular/core';
import { AuthService } from '../../../services/auth.service';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-extract',
  standalone: true,
  imports: [ButtonModule],
  templateUrl: './extract.component.html',
  styleUrl: './extract.component.scss'
})
export class ExtractComponent {

  constructor(
    private authService : AuthService,
  ){}

  logout() {
    this.authService.logout();

  }
}
