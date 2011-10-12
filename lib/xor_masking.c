#include <Python.h>
#include "Numeric/arrayobject.h"
#include <stdio.h>
#include <stdbool.h>

int main(){
Py_Initialize();
import_array();
}

static char doc[] =
"This is the C extension for xor_masking routine. It interfaces with Python via C-Api, and calculates the"
"next state with C pointer arithmetic";

	static PyObject *
	trace(PyObject *self, PyObject *args)
	{

	PyObject *input;
	PyObject *mask;
	PyObject *adjacency;
	PyObject *state;
	PyArrayObject *arr_mask;
	PyArrayObject *arr_adjacency;
	PyArrayObject *arr_state;
	PyArrayObject *arr_next_state;

	double sum;
	int counter_node, n_nodes;

	/*  PyArg_ParseTuple
	 *  checks if from args, the pointers of type "O" can be extracted, and extracts them
	 */

	if (!PyArg_ParseTuple(args, "OOO:xor_masking_C", &mask, &adjacency, &state))
		return NULL;

	/*
	 *  The pointer returned by PyArray_ContiguousFromObject is typecasted to
	 *  a PyArrayObject Pointer and array is pointed to the same address.
	 */

    arr_mask = (PyArrayObject *)
    PyArray_ContiguousFromObject(mask, PyArray_BOOL, 2, 2);
    arr_adjacency = (PyArrayObject *)
    PyArray_ContiguousFromObject(adjacency, PyArray_BOOL, 2, 2);
    arr_state = (PyArrayObject *)
    PyArray_ContiguousFromObject(state, PyArray_BOOL, 2, 2);

	if (array == NULL)
		return NULL;

	int n_mask_0 = mask->dimensions[0];
	int n_mask_1 = mask->dimensions[1];
	int n_adjacency_0 = adjacency->dimensions[0];
	int n_adjacency_1 = adjacency->dimensions[1];
	int n_state_0 = state->dimensions[0];
    int n_nodes = n_state_0;
	/*
	 * if the dimensions don't match, return NULL
	 */

    bool c_mask[n_nodes][n_nodes];

	if (n_mask_0 != n_mask_1 || n_adjacency_0 != n_adjacency_1 ||
	n_adjacency_0 != n_mask_0 || n_adjacency_0 != n_adjacency_1) {
		return NULL;
	}

	/*
	 *    The 2D arrays are introduced as follows
	 *    array[i][j] = (array->data + i*array->strides[0] + j*array->strides[1])
	 */

	for (counter_node = 0; i < n_mask; i++){
		*row_start = (array->data + i*array->strides[0]);
	}


	//Py_DECREF();

	//return PyFloat_FromDouble();
	}

static PyMethodDef TraceMethods[] = {
	{"trace", trace, METH_VARARGS, doc},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
inittrace(void)
{
    (void) Py_InitModule("trace", TraceMethods);
    import_array();
}

