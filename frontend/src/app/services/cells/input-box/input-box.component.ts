import { Component, Input } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';
import { PrimeNgModule } from '@shared/modules/prime-ng/prime-ng.module';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-input-box',
  standalone: true,
  imports: [PrimeNgModule, FormsModule],
  templateUrl: './input-box.component.html',
  styleUrl: './input-box.component.scss'
})
export class InputBoxComponent implements ICellRendererAngularComp {

  @Input() params: any;
  value: string = '';

  agInit(params: any): void {
    this.params = params;
    this.value = params.value || '';
  }

  onValueChange() {
    this.params.data[this.params.colDef.field] = this.value;
  }

  shouldDisable(): boolean {
    if (typeof this.params?.disableCondition === 'function') {
      return this.params.disableCondition(this.params.data);
    }
    return this.params.disabled || false;
  }

  refresh(params: any): boolean {
    this.params = params;
    this.value = params.value || '';
    return true;
  }
}
