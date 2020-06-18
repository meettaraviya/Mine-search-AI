# if [[ ! -f "experiments/dice_simple_5_5_5_og.txt" ]]
# then
#     python3 dice.py 5 5 5 --seed 3 --player greedy --variant simple | tee experiments/dice_simple_5_5_5_og.txt
# fi

# if [[ ! -f "experiments/dice_optimized_simple_5_5_5_og.txt" ]]
# then
#     python3 dice_optimized.py 5 5 5 --seed 3 --player greedy --variant simple | tee experiments/dice_optimized_simple_5_5_5_og.txt
# fi

# if [[ ! -f "experiments/ace_simple_5_5_5_og.txt" ]]
# then
#     python3 ace.py 5 5 5 --seed 3 --player greedy --variant simple | tee experiments/ace_simple_5_5_5_og.txt
# fi

# if [[ ! -f "experiments/figaro_simple_5_5_5_og.txt" ]]
# then
#     python3 figaro.py 5 5 5 --seed 3 --player greedy --variant simple | tee experiments/figaro_simple_5_5_5_og.txt
# fi

# if [[ ! -f "experiments/figaro_simple_5_5_5.txt" ]]
# then
#     python3 figaro.py 5 5 5 --seed 3 --player optimized_greedy --variant simple | tee experiments/figaro_simple_5_5_5.txt
# fi


# ### windows

# if [[ ! -f "experiments/dice_windows_5_5_5_og.txt" ]]
# then
#     python3 dice.py 5 5 5 --seed 3 --player greedy --variant windows | tee experiments/dice_windows_5_5_5_og.txt
# fi

# if [[ ! -f "experiments/dice_optimized_windows_5_5_5_og.txt" ]]
# then
#     python3 dice_optimized.py 5 5 5 --seed 3 --player greedy --variant windows | tee experiments/dice_optimized_windows_5_5_5_og.txt
# fi

# if [[ ! -f "experiments/ace_windows_5_5_5_og.txt" ]]
# then
#     python3 ace.py 5 5 5 --seed 3 --player greedy --variant windows | tee experiments/ace_windows_5_5_5_og.txt
# fi

# if [[ ! -f "experiments/figaro_windows_5_5_5_og.txt" ]]
# then
#     python3 figaro.py 5 5 5 --seed 3 --player greedy --variant windows | tee experiments/figaro_windows_5_5_5_og.txt
# fi


# langs=(dice dice_optimized)
# variants=(simple windows)
# for nmines in {1..64}; do
#     # for lang in "${langs[@]}"; do
#     for variant in "${variants[@]}"; do
#         # for player in "${players[@]}"; do
#         echo "python3 dice_optimized.py $nmines 8 8 --seed 0 --game_count 100 --variant $variant --player optimized_greedy"
#         python3 dice_optimized.py $nmines 8 8 --seed 0 --game_count 100 --variant $variant --player optimized_greedy 2>&1 | tee experiments/dice/dice-$nmines-$variant-$player.txt | tee -a experiments_log.out
#         # done
#     done
#     # done
# done

for size in {3..16}; do
	nmines=$(printf "%.0f" "$(($size*$size*10/64))")
	python3 dice_optimized.py $nmines $size $size --seed 0 --game_count 100 --variant windows --player optimized_greedy 2>&1 | tee experiments/dice/dice-windows-$size.txt | tee -a experiments_log.out
	python3 dice_optimized.py $nmines $size $size --seed 0 --game_count 100 --variant simple --player optimized_greedy 2>&1 | tee experiments/dice/dice-simple-$size.txt | tee -a experiments_log.out