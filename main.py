from VRP import VRP
filename = 'PL'

if __name__ == '__main__':
    print("\nWynik dla algorytmu VRP: ")
    vrp = VRP(filename)
    vrp.calculate_best_base_location()
