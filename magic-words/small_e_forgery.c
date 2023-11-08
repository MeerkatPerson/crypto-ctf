#include <string.h>
#include <gmp.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h> 

// function borrowed from the challenge author's script (magic_words.c)
char* int_to_str(mpz_t n) {
	int len = (int)mpz_sizeinbase(n, 256);
	char* res = malloc(len + 1);
	mpz_export(res, NULL, 1, 1, 0, 0, n);
	return res;
}

void string_to_int(mpz_t result, char str[], int l, mpz_t n) {

    // firstly, convert the characters to bytes
    uint8_t* bytearr = calloc(l, sizeof(uint8_t));
    // memset(&bytearr, 0, l);

    for (int i = 0; i < l; i++) {
        // we can convert a char to byte by casting it to a uint8 
        // (https://stackoverflow.com/questions/41873972/convert-from-char-to-byte)
        bytearr[i] = (uint8_t) str[i];
        // printf("Char: %c, Byte: %d\n", str[i], bytearr[i]);
    }

    // to convert a byte array to an integer (on a big-endian system - I guess we have enforced the big-endianness by how we converted the str to bytes?), we need to do:
    // uint32_t myInt1 = (bytes[0] << 24) + (bytes[1] << 16) + (bytes[2] << 8) + bytes[3];
    // https://stackoverflow.com/questions/12240299/convert-bytes-to-int-uint-in-c    

    for (int j = 0; j < l-1; j++) {
        
        // convert the byte at index j to an mpz
        mpz_t byteval;
        mpz_init(byteval);
        mpz_set_ui(byteval, bytearr[j]);

        // compute 2**eight_mult
        mpz_t two_pow_eight_mult;
        mpz_init(two_pow_eight_mult);
        mpz_ui_pow_ui(two_pow_eight_mult, 2, 8*(l-j-1));

        // multiply byteval by 2**eight_mult, which is equal to (l-1-j)*8
        mpz_t byteval_times_two_pow_eight_mult;
        mpz_init(byteval_times_two_pow_eight_mult);
        mpz_mul(byteval_times_two_pow_eight_mult, byteval, two_pow_eight_mult);

        // gmp_printf("Multiplied byteval =  %Zd by eight_mult = %Zd , result: %Zd  \n", byteval, two_pow_eight_mult, byteval_times_two_pow_eight_mult);
 
        // add to res
        mpz_add(result, result, byteval_times_two_pow_eight_mult);
        
        // clear the mpz's we no longer need
        mpz_clear(byteval);
        mpz_clear(byteval_times_two_pow_eight_mult);
        mpz_clear(two_pow_eight_mult);

    }

    mpz_t last_byteval;
    mpz_init(last_byteval);
    mpz_set_ui(last_byteval, bytearr[l-1]);

    mpz_add(result, result, last_byteval);

    // clear the mpz's we no longer need
    mpz_clear(last_byteval);

    free(bytearr);

}

int main()
{

    // check my system's endianness (https://stackoverflow.com/questions/4181951/how-to-check-whether-a-system-is-big-endian-or-little-endian) - apparently my MacOS is big endian, but my Ubuntu Docker container is little endian!
    int k = 1;
    // little endian if true
    if(*(char *)&k == 1) {printf("System is little endian!\n");};

    int e = 3;

    mpz_t e_mpz;
    mpz_init_set_str(e_mpz, "3", 0);

    mpz_t one;
    mpz_init_set_str(one, "1", 0);

    char* msg = calloc(2837, sizeof(char));

    char plain_msg[] = "ekki mike ham moo ham mike moo holy mike egg egg holy egg -- give me the flag!";

    int length = 78;

    for (int k = 0; k < length; k++) {
        msg[k] = plain_msg[k];
    }

    printf("%c\n", msg[length-1]); // sanity check - should be equal to "!"

    mpz_t n;
    mpz_init_set_str(n,	"618017787734894212297412626251373685391953260761562256145235489725638613940584232503544382290786003502312209667905128601350448023284044287685001349014156076694914712630398005605673740514051697161500094865589407030636020089742702469018865286861672757837780829537694996694833864683805379159042221723723842387709902526369317372614408759564577441603426577837263761362135010436432956275299236838020581149454958441919492440492313018496438498099089383812883390835577605611991978206224568903757920872823293843687276713402767349404190867763874002307512458092607168715450826196573891917818134117192644486518276385456954928916750027466243826789735151096947239658610479195958319740857188397997117968901882796441973903340603204071299778964190138301428335590196310114790206400024512865068139543501059161433303153043130579702895687471084173256419199357102357728600646492441278405167508180066175830384059728198376079159561904247074846373084032155551839906550032001949969880315993549738076287202881585332049659570380033962200120029734918281696120171036422629762465758525540626266912510777059762980057239483211399081674862153728665111324068484754456207003656318475064950873727298779453666117120500091671142668282469471670064268176600698035510728754159", 0);

    // I was lazy and computed the log of n in Python, it is 2836.3035965294685 apparently, so ceil to 2837 to be sure

    while(length < 2837) {

        msg[length] = '\0';

        length += 1;

        mpz_t result;
        mpz_init(result);

        string_to_int(result, msg, length, n);

        gmp_printf("Result: %Zd \n", result);

        // compute ceil(e-th root of msg_as_int)
        mpz_t root;
        mpz_init(root);
        mpz_t rem;
        mpz_init(rem);

        mpz_rootrem(root, rem, result, 3);

        mpz_t zero;
        mpz_init(zero);

        // check if there was a remainder
        if (mpz_cmp(rem, zero) > 0) {

            gmp_printf("Root before adding one: %Zd \n", root);
            mpz_add(root, root, one);
            gmp_printf("Root after adding one: %Zd \n", root);

        } 

        char* message = int_to_str(root);

        mpz_t msg_pow_e;
        mpz_init(msg_pow_e);

        mpz_powm(msg_pow_e, root, e_mpz, n);

        char* s_to_e = int_to_str(msg_pow_e);

        // I think instead of this we could have just used mpz_root which only returns non-zero if there was no remainder?
        if (strcmp(plain_msg, s_to_e) == 0) {
            gmp_printf("Found: %Zd \n", root);
            printf("s_to_e: %s \n", s_to_e);
            break;
        } else {
            printf("Not this one!\n");
        }

        mpz_clear(result);
        mpz_clear(msg_pow_e);

        free(message);
        free(s_to_e);

    }

    mpz_clear(e_mpz);
    mpz_clear(n);
    mpz_clear(one);
    free(msg);

}