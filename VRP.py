import csv
MAX_VALUE = 9999
MIN_VALUE = -999

class VRP:
    def __init__(self, file_name):                                              #wczytywanie pliku
        with open(file_name + ".csv", 'r') as file:
            reader = csv.reader(file, delimiter=";", skipinitialspace=True)
            data = list(reader)
        self.n = int(data[0][0])
        self.km_data = data[2:self.n + 2]
        self.convert_values(self.km_data)
        self.cities_data = []
        self.nodes = list(range(self.n))
        for line in data[self.n + 2:self.n + 27]:
            self.cities_data.append([line[0], line[1], line[2], line[3]])

    def convert_values(self, array):                    #konwertuje wartosci string do float
        row_index = 0
        column_index = 0
        for row_values in array:
            row_index = row_index + 1
            for value in row_values:
                column_index = column_index + 1
                array[row_index - 1][column_index - 1] = float(value.replace(',', '.'))
            column_index = 0


    def greedy(self, base_city, cities):                #algorytm zachlanny zalezny od macierzy sasiedztwa i listy miast
        available_cities = list.copy(cities)            #kopiowanie listy miast
        permutation = []                                #permutacja
        lorry_number = 1                                # numer ciężarówki
        courses_amount = 10                             # (n/K) zgodnie z założeniem stała liczba kursów dla pojazdu
        while available_cities:                         #petla do czasu posiadania miast 
            limit = True
            permutation.append(base_city)               
            j = self.find_max(available_cities, base_city)  # znajdź klienta oddalonego najdalej
            permutation.append(j)
            available_cities.remove(j)                  #usuniecie miasta j
            amount_of_order = 1                         # liczba zleceń obsłużonych przez pojazd k
            while limit:
                l = self.find_min(available_cities, j)  # znajdź miasto najbliższe miasta j
                j = l
                if amount_of_order + 1 < courses_amount:    #petla do czasu konca zamowien
                    permutation.append(l)
                    available_cities.remove(l)          #usuniecie l
                    if not available_cities:            #gdy brak dostepnych miast
                        limit = False
                    amount_of_order += 1                #zwiekszenie o 1 
                else:
                    limit = False
            lorry_number += 1                           #zwiekszenie nr ciezarowki
        permutation.append(base_city)
        return permutation
    
    def calculate_best_base_location(self):              #oblicza najlepsza lokalizacje wypisuje dane w konsoli
        best_result = MAX_VALUE
        best_result_base = 0
        best_result_perm = []
        for node in self.nodes:
            perm_result = self.greedy(node, self.nodes)         #przekazuje wynik algorytmu zachlannego
            length_of_road = self.calculate_length_of_road(perm_result) #wylicza droge
            if length_of_road < best_result:
                best_result = length_of_road                    #przypisanie wartosci wynikow
                best_result_base = node
                best_result_perm = list.copy(perm_result)
        print("Najlepsza lokacja: " + str(self.cities_data[best_result_base][1]))   #wypisywanie na ekran info
        print("Dystans do pokonania: " + str(best_result))
        print("Permutacja: " + str(best_result_perm))

    def find_max(self, list_of_available_cities, base):                 #funkcje zanjdujace max i min
        distance_from_base = list.copy(self.km_data[base])
        while distance_from_base:
            max_value = max(distance_from_base)
            index = distance_from_base.index(max_value)
            if index in list_of_available_cities:
                return index
            else:
                distance_from_base[index] = MIN_VALUE

    def find_min(self, list_of_available_cities, base):             
        distance_from_base = list.copy(self.km_data[base])
        while True:
            min_value = min(distance_from_base)
            index = distance_from_base.index(min_value)
            if index in list_of_available_cities:
                return index
            else:
                distance_from_base[index] = MAX_VALUE

    def calculate_length_of_road(self, permutation):                    #przelicz dlugosc drogi
        distance_sum = 0
        for origin, target in zip(permutation, permutation[1:]):        #petla dla permutacji
            distance_sum += self.km_data[origin][target]                
        return distance_sum                                             #zwraca dlugosc
