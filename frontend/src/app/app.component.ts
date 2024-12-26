import { Component, OnInit, HostListener } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AuthService } from './services/auth.service';
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {

  private idleTimeout: any;
  private idleTime = 10000; // 10 seconds in milliseconds

  constructor(private authService: AuthService) { }


  ngOnInit() {
    this.resetIdleTimer();

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.authService.logout();
      }
    });
  }

  @HostListener('document:mousemove')
  @HostListener('document:keypress')
  resetIdleTimer() {
    clearTimeout(this.idleTimeout);
    this.idleTimeout = setTimeout(() => {
      this.authService.logout();
    }, this.idleTime);
  }

}