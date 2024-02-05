from outbench import Outbench
from cryterion import Cryterion


def get_fake_benchmarks() -> Cryterion:
    return Cryterion(
        data_size=2,
        key_size=2,
        block_size=2,
        code_size=2,
        clock_cycles=2,
        duration=2,
        memory_usage=2,
    )


def get_random_benchmarks() -> Cryterion:
    pass


def test_outbench():
    outb = Outbench()
    outb.push_benchmarks("speck", get_fake_benchmarks())
    outb.push_benchmarks("speck", get_fake_benchmarks())

    outb.push_benchmarks("heck", get_fake_benchmarks())

    print(outb.data)

    outb.pick_best()


if __name__ == "__main__":
    test_outbench()
