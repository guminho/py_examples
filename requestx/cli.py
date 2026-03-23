from concurrent.futures import ThreadPoolExecutor
from time import monotonic

from requests import Session

URL = "http://localhost:8000/hello/{num}"


def request_run(sess: Session, num: int) -> str:
    return sess.get(URL.format(num=num)).text


def test():
    nums = range(50)
    with Session() as sess:
        with ThreadPoolExecutor(max_workers=None) as executor:
            tik = monotonic()
            results = list(executor.map(lambda n: request_run(sess, n), nums))
            tok = monotonic()
            print(f"{tok - tik:.3f}s")

    for res in results[-3:]:
        print(res)


if __name__ == "__main__":
    test()
