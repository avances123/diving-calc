import { DepthConverter } from '../physics/depth-converter';
import { SafetyStop } from '../algorithm/Options';
import { Precision } from '../common/precision';

export interface DepthLevelOptions {
    /** depth of the last stop in meters, needs to be positive number */
    lastStopDepth: number;
    safetyStop: SafetyStop;

    /**
     * Depth difference between two deco stops in metres.
     * Default is 3 meters.
     * As described in Buhlmanns Decompression book, it dated back to Navy seals in early 1900,
     * where they used 10 feet increments.
     */
    decoStopDistance: number;

    /**
     * Depth in meters, default 10 meters.
     * Emulates some computers behavior (Suunto, Mares).
     */
    minimumAutoStopDepth: number;
}

export class DepthLevels {
    constructor(private depthConverter: DepthConverter, private options: DepthLevelOptions) { }

    /**
     * Converts the pressure to depth in meters and round it to nearest deco stop
     *
     * @param depthPressure depth in bars
     */
    public toDecoStop(depthPressure: number): number {
        const depth = this.depthConverter.fromBar(depthPressure);
        return Precision.roundDistance(depth, this.options.decoStopDistance);
    }

    /**
     * returns 0 m for ascent to surface
     * currentDepth and return value in meters
     * this creates ascent using 3 meter increments
    */
    public nextStop(currentDepth: number): number {
        if (currentDepth <= this.options.lastStopDepth) {
            return 0;
        }

        const rounded = Precision.floorDistance(currentDepth, this.options.decoStopDistance);

        if (rounded !== currentDepth) {
            return rounded;
        }

        const result = currentDepth - this.options.decoStopDistance;

        if(result <= this.options.lastStopDepth) {
            return this.options.lastStopDepth;
        }

        return result;
    }

    public addSafetyStop(currentDepth: number, maxDepth: number): boolean {
        return (this.options.safetyStop === SafetyStop.always ||
                (this.options.safetyStop === SafetyStop.auto && maxDepth > this.options.minimumAutoStopDepth)) &&
                 currentDepth === this.options.lastStopDepth;
    }
}
