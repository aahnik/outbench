from cryterion import Cryterion
import pandas as pd

EVAL_C = {
    "key_size": 1,
    "block_size": 2,
    "latency_software": 5,
    "throughput_software": 1,
    "energy": 4,
    "efficiency_software": 3,
}

HIB = ["throughput_software", "efficiency_software"]  # higher is better


class Outbench:

    def __init__(self, eval_c=EVAL_C, hib=HIB):

        self.eval_c = eval_c
        self.hib = hib
        self.cols = ["algo"].append([item for item in eval_c.keys()])
        self.data = {}

    def push_benchmarks(self, algo, benchmarks: Cryterion):
        "Add new row or update existing row"

        new_row = {"algo": algo}
        for item in self.eval_c.keys():
            new_row[item] = getattr(benchmarks, item)

        self.data[algo] = new_row

    def _rank(self, verbose):
        df = pd.DataFrame(list(self.data.values()))
        # print(df)
        for item in self.eval_c.keys():
            df[f"{item}@RankScore"] = df[item].rank(ascending=(item in self.hib))
        columns_to_include = []
        for item in df.columns:
            if item.endswith("RankScore"):
                columns_to_include.append(item)
        for item in df.columns:
            df["Final Score"] = (
                df[columns_to_include]
                .multiply(
                    [self.eval_c[col.split("@")[0]] for col in columns_to_include]
                )
                .sum(axis=1)
            )
        df.sort_values("Final Score", ascending=False)
        if verbose:
            print(df)
        return df.loc[0]["algo"]

    def pick_best(self, verbose=False) -> str:
        return self._rank(verbose=verbose)
