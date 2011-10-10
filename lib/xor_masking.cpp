#include <Python.h>
#include <stdio.h>
#include <stdbool.h>

void xor_masking(bool *state, bool *mask, bool *adjacency, int size){
	
	/*
	
	*/

	for (i=0; i < size ;i++){



	}

	return 
}

static PyMethodDef PrMethods[] = {
	{"isprime", pr_isprime, METH_VARARGS, "Check if prime."},
	{NULL, NULL, 0, NULL}
};

void initpr(void){
	(void) Py_InitModule("pr", PrMethods);
}
