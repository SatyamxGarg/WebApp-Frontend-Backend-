import { inject, Injectable } from '@angular/core';
import { AuthEndpointsService } from '../../swagger/api/services';
import { BehaviorSubject, catchError, map, Observable, of } from 'rxjs';
import { Router } from '@angular/router';

const ACCESS_TOKEN_NAME = 'token';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  loggedInUserInfo = new BehaviorSubject<null | any>(null);

  private authEndpointsService: AuthEndpointsService = inject(AuthEndpointsService);
  private router: Router = inject(Router);

  isUserValid(): Observable<boolean> {
    if (!this.getAccessToken()) {
      return of(false);
    }
    return this.authEndpointsService.readUsersMeApiV1AuthUsersMeGet().pipe(
      map(response => {
        // Assuming a successful response indicates the user is valid.
        this.loggedInUserInfo.next(response.data);
        return true; // Adjust this logic as needed based on the actual response structure.
      }),
      catchError(error => {
        console.error('Error fetching user validity:', error);
        return of(false);
      })
    );
  }

  getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_NAME);
  }

  setAccessToken(token: any) {
    localStorage.setItem(ACCESS_TOKEN_NAME, token);
  }

  logout() {
    localStorage.removeItem(ACCESS_TOKEN_NAME);
    this.loggedInUserInfo.next(null);
    this.router.navigate(['auth']);
  }
}
