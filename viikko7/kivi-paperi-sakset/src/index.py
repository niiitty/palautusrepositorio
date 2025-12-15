from luo_peli import LuoPeli

def main():
    while True:
        print("Valitse pelataanko"
              "\n (a) Ihmistä vastaan"
              "\n (b) Tekoälyä vastaan"
              "\n (c) Parannettua tekoälyä vastaan"
              "\nMuilla valinnoilla lopetetaan"
              )

        vastaus = input()

        if not LuoPeli.luo_peli(vastaus):
            break


if __name__ == "__main__":
    main()
