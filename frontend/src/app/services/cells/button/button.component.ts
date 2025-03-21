import { Component, Input } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';
import { PrimeNgModule } from '@shared/modules/prime-ng/prime-ng.module';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-button',
  standalone: true,
  imports: [PrimeNgModule, FormsModule],
  templateUrl: './button.component.html',
  styleUrl: './button.component.scss'
})
export class ButtonComponent implements ICellRendererAngularComp {

  @Input() params: any;

  agInit(params: any): void {
    this.params = params;
  }

  onDelete() {
    if (this.params.onDelete) {
      this.params.onDelete(this.params.node.rowIndex);
    }
  }

  refresh(): boolean {
    return false;
  }
}