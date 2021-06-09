#define PY_SSIZE_T_CLEAN  /* For all # variants of unit formats (s#, y#, etc.) use Py_ssize_t rather than int. */
#include <Python.h>       /* MUSTֲ includeֲ <Python.h>, this implies inclusion of the following standard headers:
                             <stdio.h>, <string.h>, <errno.h>, <limits.h>, <assert.h> and <stdlib.h> (if available). */
#include <math.h>         /* includeֲ <Python.h> has to be before any standard headers are included */



typedef struct {
    double * vector_sum;
    int size;

}cluster;

double* array_copy(double*,const double*, int);
void array_2dim_copy(double **, double **,int ,int );
int array_equal(double** , double** , int ,int ) ;
double diff(const double *,const double* ,int);
int min(const double *, int);
void update_centroid(const double* , cluster*  , int, int );
void new_centroid(double**,  cluster* , int , int );
cluster* cluster_init(cluster*, int,int);
void reset_cluster(cluster* , int, int );

/*initializing clusters*/
cluster* cluster_init(cluster * clusters, int k, int d){
    int i,j;
    for (j=0;j<k; j++){
        cluster c;
        c.size=0;
        c.vector_sum = (double*) malloc(d * sizeof(double));
        assert(c.vector_sum != NULL);
        for (i=0;i<d; i++) {
            c.vector_sum[i] = 0;
        }
        clusters[j] = c;
    }
    return clusters;
}

/*copy array to other array*/
double* array_copy(double* array1,const double* array2,  int d){
    int k;
    for(k=0;k<d;k++){
        array1[k]=array2[k];
    }
    return array1;
}

/*copys 2d array to other 2d array*/
void array_2dim_copy(double **Double, double **Double1,int K,int d) {
    int l,m;
    for(l=0;l<K;l++){
        for(m=0;m<d;m++){
            Double[l][m]=Double1[l][m];
        }
    }
}

/*checks if 2 arrays are equal*/
int array_equal(double** prev_array, double** curr_array, int k,int d) {
    int p,r;
    for (p = 0; p < k; p++) {
        for (r = 0; r < d; r++) {
            if (prev_array[p][r] != curr_array[p][r]) {
                return 0;
            }
        }
    }
    return 1;
}

/*returns the index of the min*/
int min(const double *array, int k) {
    int r, index;
    double min;
    index = 0;
    min = array[0];
    for(r=0;r<k;r++){
        if (array[r] < min){
            index = r;
            min = array[r];
        }
    }
    return index;
}

/*calculates the distance between 2 vectors*/
double diff(const double * vector1,const double * vector2,int d){
    double sum;
    int j;
    sum=0;
    for (j=0;j<d;j++){
        sum+=(vector1[j]-vector2[j])*(vector1[j]-vector2[j]);
    }
    return sum;

}
/*updates the vector_sum field when new vector is added*/
void update_centroid(const double* vector, cluster * clusters,int min_index, int d){
    int q;
    for (q=0;q<d;q++){
        clusters[min_index].vector_sum[q]+=vector[q];
    }

}
/*calculates the new centroids*/
void new_centroid(double **curr_cent,  cluster* clusters, int k, int d) {
    int i,j;
    for(i=0; i<k; i++){
        for (j=0;j<d;j++){
            if (clusters[i].size==0){
                curr_cent[i][j] = clusters[i].vector_sum[j]/1;
            }
            else{
                curr_cent[i][j] = clusters[i].vector_sum[j]/ (float)clusters[i].size;
            }
        }
    }
}


/*resets the clusters by filling with 0s*/
void reset_cluster(cluster* cluster1, int k,  int d) {
    int x,y;
    for(y=0;y<k;y++) {
        cluster1[y].size=0;
        for (x = 0; x < d; x++) {
            cluster1[y].vector_sum[x] = 0;
        }
    }
}

double** main_c(int K,int N,int d,int max_iter, double ** vectors,double ** centroids) {

    int cnt;
    int e, m;
    int r;
    int p;
    int x, b;
    double *distance;
    cluster *clusters;
    double **prev_centroids;

    distance = (double *) malloc(K * sizeof(double));
    assert(distance != NULL);
    clusters = (cluster *) malloc(K * sizeof(cluster));
    assert(clusters != NULL);
    prev_centroids = (double **) malloc(K * sizeof(double *));
    assert(prev_centroids != NULL);

    clusters = cluster_init(clusters, K, d);

    for (e = 0; e < K; e++) {
        prev_centroids[e] = (double *) malloc(d * sizeof(double));
        assert(prev_centroids[e] != NULL);
        for (m = 0; m < d; m++) {
            prev_centroids[e][m] = 0;
        }
    }

    cnt = 0;
    while (cnt < max_iter && !array_equal(centroids, prev_centroids, K, d)) { /*the main function*/
        array_2dim_copy(prev_centroids, centroids, K, d);
        reset_cluster(clusters, K, d);
        for (x = 0; x < N; x++) {
            int min_index;
            for (b = 0; b < K; b++) {
                distance[b] = diff(vectors[x], prev_centroids[b], d);
            }
            min_index = min(distance, K);
            update_centroid(vectors[x], clusters, min_index, d);
            clusters[min_index].size++;
        }
        new_centroid(centroids, clusters, K, d);
        cnt++;
    }

    free(distance);
    distance = NULL;

    for (p = 0; p < N; p++) {
        free(vectors[p]);
        vectors[p] = NULL;
    }
    free(vectors);
    vectors = NULL;

    for (p = 0; p < K; p++) {
        free(prev_centroids[p]);
        prev_centroids[p] = NULL;
    }
    free(prev_centroids);
    prev_centroids = NULL;

    for (r = 0; r < K; r++) {
        free(clusters[r].vector_sum);
        clusters[r].vector_sum = NULL;
    }
    free(clusters);
    clusters = NULL;

    return centroids;
}
    /*
 * API functions
 */


    static PyObject* fit_capi(PyObject *self, PyObject *args)
    {
        PyObject *_list, *_list2;
        PyObject *item, *item2, *item3;
        int k,n,d,max;
        double ** vectors;
        double ** centroids;
        double ** new_centroids;
        double ** more_centroids;
        int i,j;

        if(!PyArg_ParseTuple(args, "iiiiOO", &k,&n,&d,&max,&_list,&_list2)) {
            return NULL;
        }

        PyObject *result_lst = PyList_New(k);
        vectors = (double **) malloc(n* sizeof(double *));
        centroids = (double **) malloc(k * sizeof(double *));
        new_centroids = (double **) malloc(k * sizeof(double *));
        more_centroids = (double **) malloc(k * sizeof(double *));

        /* Is it a list? */
        if (!PyList_Check(_list)||!PyList_Check(_list2)||!PyList_Check(result_lst)) {
            return NULL;
        }

        for (i = 0; i < k; i++) {
            item = PyList_GetItem(_list2, i);
            PyObject *item_inside;
            double* centroid = malloc(d * sizeof(double));
            assert(centroid != NULL);
            for (j = 0; j < d; j++) {
                item_inside = PyList_GetItem(item, j);
                centroid[j] = PyFloat_AsDouble(item_inside);
            }
            centroids[i] = centroid;
        }

        for (i = 0; i < n; i++) {
            item2 = PyList_GetItem(_list, i);
            PyObject *item_inside;
            double* x_i = malloc(d * sizeof(double));
            assert(x_i != NULL);
            for (j = 0; j < d; j++) {
                item_inside = PyList_GetItem(item2, j);
                x_i[j] = PyFloat_AsDouble(item_inside);
            }
            vectors[i] = x_i;
        }

        new_centroids = main_c(k,n,d,max, vectors, centroids);

        for (i = 0; i < k; i++) {
            PyObject *vec_lst = PyList_New(d);
            if (!vec_lst) {
                return NULL;
            }
            for (j = 0; j < d; j++) {
                PyObject *num = PyFloat_FromDouble(new_centroids[i][j]);
                if (!num) {
                    Py_DECREF(num);
                    return NULL;
                }
                PyList_SetItem(vec_lst,j,num);
            }
            PyList_SetItem(result_lst,i,vec_lst);
        }
        return result_lst;
    }

/*
 * This array tells Python what methods this module has.
 * We will use it in the next structure
 */

    static PyMethodDef capiMethods[] = {
            {"fit",                   /* the Python method name that will be used */
                    (PyCFunction)  fit_capi, /* the C-function that implements the Python function and returns static PyObject*  */
                         METH_VARARGS,           /* flags indicating parameters
accepted for this function */
                            PyDoc_STR("A geometric series up to n. sum_up_to_n(z^n)")}, /*  The docstring for the function */
            {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all                                 of the functions for the module have been defined. */
    };




/* This initiates the module using the above definitions. */
    static struct PyModuleDef moduledef = {
            PyModuleDef_HEAD_INIT,
            "mykmeanssp", /* name of module */
            NULL, /* module documentation, may be NULL */
            -1,  /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
            capiMethods /* the PyMethodDef array from before containing the methods of the extension */
    };

    PyMODINIT_FUNC
    PyInit_mykmeanssp(void)
    {
        PyObject *n;
        n = PyModule_Create(&moduledef);
        if (!n) {
            return NULL;
        }
        return n;
    }

