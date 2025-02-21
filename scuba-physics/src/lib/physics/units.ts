/** All values are in respective units */
export interface Units {
    name: string;
    lengthShortcut: string;
    pressureShortcut: string;
    volumeShortcut: string;
    weightShortcut: string;
    altitudeShortcut: string;
    densityShortcut: string;
    toMeters(length: number): number;
    fromMeters(meters: number): number;
    toBar(pressure: number): number;
    fromBar(bars: number): number;
    toLiter(volume: number): number;
    fromLiter(liters: number): number;
    /** Converts volume of tank based on working pressure in bars */
    fromTankLiters(liters: number, workingPressure: number): number;
    /** Converts volume of tank based on working pressure in bars */
    toTankLiters(cuftVolume: number, workingPressure: number): number;

    fromGramPerLiter(density: number): number;

    toGramPerLiter(density: number): number;

    fromKilogram(weight: number): number;

    toKilogram(weight: number): number;
}

/**
 * 1:1 adapter transforming metric units to metric units. This is a dummy adapter for metric units usage,
 * which we don't convert, because all calculations are done in metric units by default.
 */
export class MetricUnits implements Units {
    public get name(): string {
        return 'Metric';
    }

    public get lengthShortcut(): string{
        return 'm';
    }

    public get pressureShortcut(): string {
        return 'bar';
    }

    public get volumeShortcut(): string{
        return 'l';
    }

    public get weightShortcut(): string{
        return 'kg';
    }

    public get altitudeShortcut(): string{
        return 'm.a.s.l';
    }

    public get densityShortcut(): string{
        return 'g/l';
    }

    public toMeters(length: number): number {
        return length;
    }

    public fromMeters(meters: number): number {
        return meters;
    }

    public toBar(pressure: number): number {
        return pressure;
    }

    public fromBar(bars: number): number {
        return bars;
    }

    public toLiter(volume: number): number {
        return volume;
    }

    public fromLiter(liters: number): number {
        return liters;
    }

    public fromTankLiters(liters: number): number {
        return liters;
    }

    public toTankLiters(cuftVolume: number): number {
        return cuftVolume;
    }

    public fromGramPerLiter(density: number): number {
        return density;
    }

    public toGramPerLiter(density: number): number {
        return density;
    }

    public fromKilogram(weight: number): number {
        return weight;
    }

    public toKilogram(weight: number): number {
        return weight;
    }
}

/**
 * length: meter/foot
 * https://en.wikipedia.org/wiki/Foot_(unit)
 * 1 foot = 0.3048 meter - derived international foot
 * Altitude m.a.s.l. to f.a.s.l. is only conversion from meters to feet
 *
 * volume: cubic foot (cft)/liter
 * https://en.wikipedia.org/wiki/Standard_cubic_foot
 * https://en.wikipedia.org/wiki/Cubic_foot
 * 1 cft = 28.316846592 liter
 *
 * pressure: bar/psi
 * https://en.wikipedia.org/wiki/Pound_per_square_inch
 * 1 bar = 14.503773773022 psi
*/
export class ImperialUnits implements Units {
    private static readonly psiRate = 14.503773773022;
    private static readonly cftRate = 28.316846592;
    private static readonly lbRate = 2.20462262185;

    /**
     * 1 fsw equals 0.30643 msw
     * consider distinguish m and ft from msw and fsw https://en.wikipedia.org/wiki/Metre_sea_water
     */
    private static readonly footRate = 0.3048;
    /** 1 gram to pound */
    private static readonly poundRate = 0.00220462262;
    /** 1 g/l  = cca 0.06242796 lb/cuft */
    private static readonly lbPerCuftRate = ImperialUnits.poundRate * ImperialUnits.cftRate;

    public get name(): string{
        return 'Imperial';
    }

    public get lengthShortcut(): string{
        return 'ft';
    }

    public get pressureShortcut(): string {
        return 'psi';
    }

    public get volumeShortcut(): string{
        return 'cuft';
    }

    public get weightShortcut(): string{
        return 'lb';
    }

    public get altitudeShortcut(): string{
        return 'ft.a.s.l';
    }

    public get densityShortcut(): string{
        return 'lb/cuft';
    }

    public toMeters(length: number): number {
        return length * ImperialUnits.footRate;
    }

    public fromMeters(meters: number): number {
        return meters / ImperialUnits.footRate;
    }

    public toBar(pressure: number): number {
        return pressure / ImperialUnits.psiRate;
    }

    public fromBar(bars: number): number {
        return bars * ImperialUnits.psiRate;
    }

    public toLiter(volume: number): number {
        return volume * ImperialUnits.cftRate;
    }

    public fromLiter(liters: number): number {
        return liters / ImperialUnits.cftRate;
    }

    public fromTankLiters(liters: number, workingPressure: number): number {
        const relativeVolume = this.fromLiter(liters);
        const absoluteVolume = relativeVolume * workingPressure;
        return absoluteVolume;
    }

    public toTankLiters(cuftVolume: number, workingPressure: number): number {
        // S80 => 11.1 L  => 80 cuft at 3000 psi
        // 80 cuft -> 2265.3 L, 3000 psi -> 206.84 b => 2265.3/206.84 = 10.95 L
        const absoluteLiters = this.toLiter(cuftVolume);
        const newLiters = absoluteLiters / workingPressure;
        return newLiters;
    }

    public fromGramPerLiter(density: number): number {
        return density * ImperialUnits.lbPerCuftRate;
    }

    public toGramPerLiter(density: number): number {
        return density / ImperialUnits.lbPerCuftRate;
    }

    public fromKilogram(weight: number): number {
        return weight * ImperialUnits.lbRate;
    }

    public toKilogram(weight: number): number {
        return weight / ImperialUnits.lbRate;
    }
}
