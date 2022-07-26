import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  userCredentials: string | undefined;

  constructor() { }

  getUsername(): string {

    // TODO change
    this.userCredentials = 'pan.doktor@pg.edu.pl:1234'
    //atob(this.userCredentials).split(':')[0];
    // @ts-ignore
    return this.userCredentials.split(':')[0];
  }

}
