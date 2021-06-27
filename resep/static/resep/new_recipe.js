document.querySelector('#ingbtn').addEventListener('click', addform);
var form_id = 3;
function addform()  {
	form_id++;
    var input = document.createElement("input");
	input.className = 'form_bahan_list form-control'
	input.id = 'ing-' + form_id;
    input.type = 'text';
    input.name = 'ing';
    input.placeholder = 'bahan ' + form_id;
	document.querySelector('#ingadd').appendChild(input);
  };

document.querySelector('#stepbtn').addEventListener('click', addstep);
var step = 3;
function addstep()  {
	step++;
    var input = document.createElement("textarea");
	input.className = 'form_bahan_list form-control'
	input.id = 'step-' + step;
    input.type = 'text';
    input.name = 'step';
    input.placeholder = 'Langkah ' + step;
	document.querySelector('#stepadd').appendChild(input);
  };