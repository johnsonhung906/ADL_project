#!/bin/bash
CUDA_VISIBLE_DEVICES=$1 \
python3 simulator.py \
--model_name_or_path ./bigdataset_base/checkpoint-10000 \
--max_len 50 \
--num_beams 10 \
--num_chats 50 \
--disable_output_dialog \
--output ./bigdataset_base/output_cp-10000.jsonl