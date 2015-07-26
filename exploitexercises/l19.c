#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main() {
        int a = fork();
        char * const argv[] = {"/home/flag19/flag19", "-c", "/usr/bin/id", NULL};
        char * const envp[] = {NULL};

        //This is the child
        if (a == 0){
                int newfd = open("/tmp/a1", 'w');
                printf("Newfd is %d\n", newfd);
                //dup2(newfd, 1);
                sleep(1);
                printf("Child PID is %d\n",getpid());
                printf("Parent process ID before running flag19 is %d\n", getppid());
                int x = execve("/home/flag19/flag19", argv, envp);
                if (x == -1){
                        printf("Execve failed\n");
                }
        }
        //This is the parent
        else{
                printf("Parent PID is %d\n",getpid());
                return 0;
        }
}

