/*
 * hashcode_solver.cpp
 *
 *  Created on: 29 February, 2020
 *  Author(s): Ahmed Morsy & Amr ELzawawy
 */
#include <unordered_map>
#include <iostream>
#include <algorithm>
#include <string>
#include <vector>
#include <math.h>
#include <map>
#include <set>

#include "hashcode_solver.h"
#define mp make_pair
using namespace std;

int num_libraries,num_days,num_books;           // integer variables.
int book_scores[N],library_num_books[N],library_sign_days[N],library_books_per_day[N];  //array integer variables.
vector<int> library_books[N],books_relation[N];     // vector integer variables.
vector<pair<int,int> >library_sorted_books[N];      // vector pair of integers variables.

void read_input(char* input_filename){
    freopen(input_filename,"r",stdin);
    // Input First line: num_books - num_libraries - num_days_allowed
    scanf("%d %d %d",&num_books,&num_libraries,&num_days);
    // Input Second line: scores for each book.
    for(int i = 0 ;i < num_books ; i++)
        scanf("%d",&book_scores[i]);
    // For each library, two lines
    for(int i = 0 ; i < num_libraries ; i++){
        // Library Line One: num_books - sign process days - books per day
        scanf("%d %d %d",&library_num_books[i],&library_sign_days[i],&library_books_per_day[i]);
        // Library Line Two: books ids to define books in this library
        for(int j = 0; j < library_num_books[i] ; j++){
            int book_id;
            scanf("%d",&book_id);
            library_books[i].push_back(book_id);
            library_sorted_books[i].push_back(mp(book_scores[book_id],book_id));
            // 
            books_relation[book_id].push_back(i);
        }
        // Sort books scores for each library according to descending order.
        sort(library_sorted_books[i].begin(), library_sorted_books[i].end(), greater<>());
    }
}

void solve_problem(char* output_filename){
    int current_day = 0;
    vector<bool> taken_libraries(num_libraries,0);
    vector<bool> taken_books(num_books,0);
    vector<int> library_history;
    vector<int> books_ids[N];

   for(int library_id_outer = 0 ; library_id_outer < num_libraries ; library_id_outer++){
        if(current_day > num_days) 
            break;
        int best = -1;
        long long factor_nominator = 0, factor_denominator = 1;
        vector<int>lib_score(num_libraries,0);

        for(int library_id_inner = 0 ; library_id_inner < num_libraries ; library_id_inner++){
            if(taken_libraries[library_id_inner])
                continue;
            for(int k = 0 ; k < library_books[library_id_inner].size() ; k++){
                int book_id = library_books[library_id_inner][k];
                if(taken_books[book_id])
                    continue;
                lib_score[library_id_inner]+= book_scores[book_id];
            }
        }

        for(int j = 0 ; j < num_libraries ;j++){
            if(taken_libraries[j])
                continue;
            if(best == -1){
                best = j;
                factor_nominator = lib_score[j];
                factor_denominator = library_sign_days[j];
            }
            else{
                if(factor_nominator*library_sign_days[j] < factor_denominator*lib_score[j]){
                    best = j;
                    factor_nominator = lib_score[j];
                    factor_denominator = library_sign_days[j];
                }
            }
        }

        if(best != -1)
            current_day += library_sign_days[best];
        else{
            break;
        }

        if(current_day < num_days){
            library_history.push_back(best);
            taken_libraries[best] = true;
            bool any = false;
            int total = 0, cur_day2 = current_day;
            for(int j = 0 ; j < library_books[best].size() ; j++){
                int book_id = library_sorted_books[best][j].second;
                if(cur_day2 == num_days)
                    break;
                if(!taken_books[book_id]){
                        books_ids[(int)library_history.size()-1].push_back(book_id);
                        total++;
                        any = true;
                }
                if(total == library_books_per_day[best]){
                    total = 0;
                    cur_day2++;
                }
                taken_books[book_id] = true;
            }
            if(!any)library_history.pop_back();
        }
   }

   freopen(output_filename,"w",stdout);
   printf("%d\n",(int)library_history.size());
   for(int i=0;i<library_history.size();i++){
      printf("%d %lu\n",library_history[i], books_ids[i].size());
      for(int j=0;j<books_ids[i].size();j++){
        printf("%d ",books_ids[i][j]);
      }
      printf("\n");
   }
}
