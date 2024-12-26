const shell = require('shelljs');
const instance = process.argv.slice(-1)[0];
let environment = require('../environments/environment');
switch (instance) {
  case 'dev':
    environment = require('../environments/environment');
    break;
  default:
    environment = require('../environments/environment');
}

const api = `ng-openapi-gen --input ./src/console/openapi.json --output ./src/swagger/api`;
shell.exec(api);
