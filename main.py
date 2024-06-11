import converter

def main():
    con = converter.Converter()
    block_arr = con.readInput()
    con.output(con.commandify(block_arr))

if __name__ == "__main__":
    main()