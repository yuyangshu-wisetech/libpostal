#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#include "libpostal.h"
#include "log/log.h"
#include "scanner.h"

int main(int argc, char **argv) {
    if (argc < 3) {
        log_error("Usage: test_libpostal string languages...\n");
        exit(EXIT_FAILURE);
    }

    char *str = argv[1];
    char *languages[argc - 2];
    for (int i = 0; i < argc - 2; i++) {
        char *arg = argv[i + 2];
        if (strlen(arg) >= MAX_LANGUAGE_LEN) {
            printf("arg %d was longer than a language code (%d chars). Make sure to quote the input string\n", i + 2, MAX_LANGUAGE_LEN - 1);
        }
        languages[i] = arg;
    }

    if (!libpostal_setup()) {
        exit(EXIT_FAILURE);
    }

    normalize_options_t options = {
        .num_languages = 1,
        .languages = languages,
        .address_components = ADDRESS_HOUSE_NUMBER | ADDRESS_STREET | ADDRESS_UNIT,
        .latin_ascii = 1,
        .transliterate = 1,
        .strip_accents = 1,
        .decompose = 1,
        .lowercase = 1,
        .trim_string = 1,
        .replace_word_hyphens = 1,
        .delete_word_hyphens = 0,
        .replace_numeric_hyphens = 0,
        .delete_numeric_hyphens = 0,
        .split_alpha_from_numeric = 1,
        .delete_final_periods = 1,
        .delete_acronym_periods = 1,
        .drop_english_possessives = 1,
        .delete_apostrophes = 1,
        .expand_numex = 1,
        .roman_numerals = 1
    };

    uint64_t num_expansions;

    char **strings;
    char *normalized;

    int num_loops = 100000;

    token_array *tokens = tokenize(str);
    uint64_t num_tokens = tokens->n;
    token_array_destroy(tokens);

    clock_t t1 = clock();
    for (int i = 0; i < num_loops; i++) {
        strings = expand_address(str, options, &num_expansions);
        for (uint64_t i = 0; i < num_expansions; i++) {
            normalized = strings[i];
            free(normalized);
        }
        free(strings);
    }
    clock_t t2 = clock();

    double benchmark_time = (double)(t2 - t1) / CLOCKS_PER_SEC;
    printf("Benchmark time: %f\n", benchmark_time);
    double addresses_per_second = num_loops / benchmark_time;
    printf("addresses/s = %f\n", addresses_per_second);
    double tokens_per_second = (num_loops * num_tokens) / benchmark_time;
    printf("tokens/s = %f\n", tokens_per_second);
    libpostal_teardown();
}
