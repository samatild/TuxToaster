# cpu/cpu_stress.py

def cpu_stress():
    a, b = 0, 1
    for _ in range(10**7):  # Adjust the range as needed
        a, b = b, a + b


if __name__ == "__main__":
    cpu_stress()
