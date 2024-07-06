import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { CounterModule } from './features/counter/counter.module';
import { ApiService } from './services/api.service';

@Component({
  standalone: true,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  imports: [
    RouterModule,
    StoreModule,
    EffectsModule,
    StoreDevtoolsModule,
    CounterModule,
  ],
})
export class AppComponent implements OnInit {
  title: string = 'Loading...';

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.apiService.getData().subscribe(
      (data) => {
        this.title = data.title;
      },
      (error) => {
        console.error('Error:', error);
        this.title = 'Error loading data';
      }
    );
  }
}
