class ItemValue:
    def __init__(self, wt, val):
        self.wt = wt
        self.val = val
        self.cost = val / wt

    def __lt__(self, other):
        return self.cost < other.cost


class FractionalKnapSack:

    @staticmethod
    def getMaxValue(wt, val, capacity):
        items = []

        for i in range(len(wt)):
            items.append(ItemValue(wt[i], val[i]))

        items.sort(reverse=True)

        totalValue = 0

        for item in items:
            if capacity >= item.wt:
                capacity -= item.wt
                totalValue += item.val
            else:
                fraction = capacity / item.wt
                totalValue += item.val * fraction
                break

        return totalValue


wt = [10, 40, 20, 30]
val = [60, 40, 100, 120]
capacity = 50

maxValue = FractionalKnapSack.getMaxValue(wt, val, capacity)

print("Maximum possible value =", maxValue)