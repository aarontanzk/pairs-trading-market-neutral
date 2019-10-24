def splitData(equity1, equity2):
    print("-------------------------- RUNNING SPLITDATA() --------------------------------")
    eq1 = getAverageAlphaVantageDataframe(equity1)
    eq2 = getAverageAlphaVantageDataframe(equity2)

    ratios = eq1 / eq2
    print(len(ratios))
    train = ratios[:1762]
    test = ratios[1762:]

    ratios_mavg5 = train.rolling(window=5,center=False).mean()
    ratios_mavg60 = train.rolling(window=60,center=False).mean()
    std_60 = train.rolling(window=60,center=False).std()
    zscore_60_5 = (ratios_mavg5 - ratios_mavg60)/std_60
    plt.figure(figsize=(15,7))
    plt.plot(train.index, train.values)
    plt.plot(ratios_mavg5.index, ratios_mavg5.values)
    plt.plot(ratios_mavg60.index, ratios_mavg60.values)
    plt.legend(['Ratio','5d Ratio MA', '60d Ratio MA'])
    plt.ylabel('Ratio')
    plt.show()
