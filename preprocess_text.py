import time
import multiprocessing as mp
import pandas as pd
from utils import read_comments, cleanup_text


def main():
    texts = read_comments('./comments.csv', 'text')['text']
    print(f"Total number of comments to be processed: {len(texts)}")

    ts = time.perf_counter()
    texts.map(cleanup_text)
    print(f"Time taken to cleanup texts without multiprocessing (pandas map) : {time.perf_counter() - ts}")

    with mp.Pool(mp.cpu_count()) as pool:
        ts = time.perf_counter()
        pool.map_async(cleanup_text, texts).get()
        print(f"Time taken with multiprocessing (map_async): {time.perf_counter() - ts}")

        ts = time.perf_counter()
        clean_text = pool.imap(cleanup_text, texts, chunksize=280)
        print(f"Time taken with multiprocessing (imap): {time.perf_counter() - ts}")

        ts = time.perf_counter()
        pool.imap_unordered(cleanup_text, texts, chunksize=280)
        print(f"Time taken with multiprocessing (imap_unordered): {time.perf_counter() - ts}")

        text_ser = pd.Series(clean_text)
        print(text_ser)


if __name__ == '__main__':
    main()
