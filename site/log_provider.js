const { DateTime } = require('luxon')

class LogProvider {
    constructor() {
        this._listeners = new Map()
        this._cache = new Map()
        this._pending = new Set()
    }

    addListener(name, listener) {
        this._listeners.set(name, listener)
    }

    removeListener(name) {
        this._listeners.delete(name)
    }

    getLog(datetime) {
        return this._fromCache(datetime)
    }

    _fromCache(datetime) {
        if (this._cache.has(datetime)) {
            return this._cache.get(datetime)
        }

        if (!this._pending.has(datetime)) {
            this._apiFetch(datetime)
        }

        return {
            status: 'LOADING',
            value: null,
        }
    }

    async _apiFetch(datetime) {
        this._pending.add(datetime)

        const filename_string = DateTime.fromISO(datetime, {setZone: true}).toFormat('y_MM_dd_HH')
        const url = `https://storage.googleapis.com/kanjiapi-popularity-contest/${filename_string}`
        const response = await fetch(url);

        this._cache = this._cache.set(
            datetime,
            {
                status: response.status === 200 ? 'SUCCESS' : 'ERROR',
                value: response.status === 200 ?
                await response.json() :
                response.status,
            },
        )

        for (const listener of this._listeners.values()) {
            listener()
        }
    }
}

module.exports = {
    LogProvider,
};
