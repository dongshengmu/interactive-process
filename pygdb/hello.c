#include "stdio.h"

typedef struct fpc {
    int fpc_slot;
} fpc_t;

typedef struct mod_table {
    int     item_count;
    char    name[32];
} mod_table_t;


mod_table_t toolkit = {
    item_count: 0x1f,
    name:       "Module toolkit"
};

mod_table_t *module_node_toolkit_table = &toolkit;


void ukern_module_init(void)
{
    return;
}

void cmfwdd_pic_online(fpc_t *msg)
{
    int i = 0;
    while (1) {
        i++;
    }
}

int main(void)
{
    int mylocal = 500;

    printf("Hello, Python controlled GDB for white-box test.\n");
    ukern_module_init();
    printf("mylocal is %d\n", mylocal);
    cmfwdd_pic_online(NULL);
    return mylocal * 4;
}

