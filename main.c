#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    char name[20];
    int hp;
    int max_hp;
    int attack;
    int defense;
} Character;

void print_status(Character *c) {
    printf("%s: HP %d/%d\n", c->name, c->hp, c->max_hp);
}

int attack(Character *attacker, Character *defender) {
    int damage = attacker->attack - defender->defense;
    if (damage < 1) damage = 1;
    defender->hp -= damage;
    if (defender->hp < 0) defender->hp = 0;
    printf("%sの攻撃！\n", attacker->name);
    printf("%sに%dのダメージ！\n", defender->name, damage);
    return damage;
}

int main() {
    srand(time(NULL));

    Character hero = {"ゆうしゃ", 30, 30, 10, 3};
    Character slime = {"スライム", 20, 20, 5, 1};

    printf("=== ドラクエ風バトル開始！ ===\n");

    while (hero.hp > 0 && slime.hp > 0) {
        int command;
        printf("\nコマンドを選んでください:\n");
        printf("1: たたかう  2: にげる\n");
        scanf("%d", &command);

        if (command == 1) {
            attack(&hero, &slime);
            if (slime.hp <= 0) {
                printf("\n%s を たおした！\n", slime.name);
                break;
            }

            attack(&slime, &hero);
            if (hero.hp <= 0) {
                printf("\n%s は やられてしまった...\n", hero.name);
                break;
            }

            printf("\n--- ステータス ---\n");
            print_status(&hero);
            print_status(&slime);
        } else if (command == 2) {
            if (rand() % 2 == 0) {
                printf("\nうまく にげられた！\n");
                break;
            } else {
                printf("\nにげられなかった！\n");
                attack(&slime, &hero);
                if (hero.hp <= 0) {
                    printf("\n%s は やられてしまった...\n", hero.name);
                    break;
                }
            }
        } else {
            printf("無効なコマンドです。\n");
        }
    }

    printf("\n=== バトル終了 ===\n");
    return 0;
}
