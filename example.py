# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.
import os
from typing import Optional
from timeit import default_timer as timer
from datetime import timedelta

import fire
import torch

from llama import Llama


def main(
    ckpt_dir: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'llm_model'),
    tokenizer_path: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'llm_model', 'tokenizer.model'),
    temperature: float = 0.2,
    top_p: float = 0.95,
    max_seq_len: int = 512,
    max_batch_size: int = 4,
    max_gen_len: Optional[int] = None,
):
    start = timer()
    print(f"Have cuda?: {torch.cuda.is_available()}")

    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    instructions = [
        [
            {
                "role": "user",
                "content": "Write a C code function for calculating a fibonacci sequence.",
            }
        ],
        [
            {
                "role": "user",
                "content": "Also provide an answer in C#.",
            }
        ],
       # [
       #     {
       #         "role": "user",
       #         "content": "What is the difference between inorder and preorder traversal? Give an example in Python.",
       #     }
       # ],
       # [
       #     {
       #         "role": "system",
       #         "content": "Provide answers in JavaScript",
       #     },
       #     {
       #         "role": "user",
       #         "content": "Write a function that computes the set of sums of all contiguous sublists of a given list.",
       #     }
       # ],
    ]
    results = generator.chat_completion(
        instructions,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    for instruction, result in zip(instructions, results):
        print(result['generation']['content'])
        #for msg in instruction:
        #    print(f"{msg['role'].capitalize()}: {msg['content']}\n")
        #print(
        #    f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
        #)
        #print("\n==================================\n")
    print(f"Elapsed Time (sec): { timedelta(seconds=(timer()-start)) }")

if __name__ == "__main__":
    fire.Fire(main)
