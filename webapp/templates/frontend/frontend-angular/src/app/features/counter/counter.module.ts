import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CounterRoutingModule } from './counter-routing.module';
import { CounterComponent } from './components/counter/counter.component';

@NgModule({
  declarations: [CounterComponent],
  imports: [CommonModule, CounterRoutingModule],
  exports: [CounterComponent],
})
export class CounterModule {}
