import { Component, Input } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';
import { PrimeNgModule } from '@shared/modules/prime-ng/prime-ng.module';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dropdown',
  standalone: true,
  imports: [PrimeNgModule, FormsModule],
  templateUrl: './dropdown.component.html',
  styleUrl: './dropdown.component.scss'
})
export class DropdownComponent implements ICellRendererAngularComp {

  @Input() params: any;
  options: any[] = [];
  selectedValue: string = '';

  agInit(params: any): void {
    this.params = params;
    this.options = params.options;
    this.selectedValue = params.value;
  }

  onValueChange(event: any) {
    this.params.data[this.params.colDef.field] = event.value;
    this.params.api.refreshCells({ rowNodes: [this.params.node] });
  }

  refresh(params: any): boolean {
    return false;
  }
}
