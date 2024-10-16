import { GroupTaskQueue } from '@baserow/modules/core/utils/queue'

// Create a custom sense of time that can be controlled by the test
// and don't rely on some precise timing that could fail in CI.
function startTimer(timer) {
  if (timer.timerInterval) {
    clearInterval(timer.timerInterval)
  }
  timer.currentTime = 0
  timer.timerInterval = setInterval(() => {
    timer.currentTime += 5
  }, 5)
}

function stopTimer(timer) {
  if (timer.timerInterval) {
    clearInterval(timer.timerInterval)
    timer.timerInterval = null
  }
}

function sleep(timer, ms) {
  const targetTime = timer.currentTime + ms
  return new Promise((resolve) => {
    const checkTime = () => {
      if (timer.currentTime >= targetTime) {
        resolve()
      } else {
        setTimeout(checkTime, 2)
      }
    }
    checkTime()
  })
}

describe('test GroupTaskQueue when immediately filling the queue', () => {
  let timer

  beforeAll(() => {
    timer = { currentTime: 0, timerInterval: null }
    startTimer(timer)
  })

  afterAll(() => {
    stopTimer(timer)
  })

  test('test GroupTaskQueue when immediately filling the queue', async () => {
    let executed1 = false
    let executed2 = false

    const queue = new GroupTaskQueue()
    queue.add(async () => {
      await sleep(timer, 20)
      executed1 = true
    })
    queue.add(async () => {
      await sleep(timer, 20)
      executed2 = true
    })

    expect(executed1).toBe(false)
    expect(executed2).toBe(false)

    await sleep(timer, 15)

    expect(executed1).toBe(false)
    expect(executed2).toBe(false)

    await sleep(timer, 10)

    expect(executed1).toBe(true)
    expect(executed2).toBe(false)

    await sleep(timer, 20)

    expect(executed1).toBe(true)
    expect(executed2).toBe(true)
  })
})
describe('test GroupTaskQueue adding to queue on the fly', () => {
  let timer

  beforeAll(() => {
    timer = { currentTime: 0, timerInterval: null }
    startTimer(timer)
  })

  afterAll(() => {
    stopTimer(timer)
  })
  test('test GroupTaskQueue adding to queue on the fly', async () => {
    let executed1 = false
    let executed2 = false
    let executed3 = false

    const queue = new GroupTaskQueue()
    queue.add(async () => {
      await sleep(timer, 20)
      executed1 = true
    })

    expect(executed1).toBe(false)
    expect(executed2).toBe(false)
    expect(executed3).toBe(false)

    await sleep(timer, 15)

    expect(executed1).toBe(false)
    expect(executed2).toBe(false)
    expect(executed3).toBe(false)

    queue.add(async () => {
      await sleep(timer, 20)
      executed2 = true
    })

    await sleep(timer, 15)

    expect(executed1).toBe(true)
    expect(executed2).toBe(false)
    expect(executed3).toBe(false)

    queue.add(async () => {
      await sleep(timer, 20)
      executed3 = true
    })

    await sleep(timer, 15)

    expect(executed1).toBe(true)
    expect(executed2).toBe(true)
    expect(executed3).toBe(false)

    await sleep(timer, 25)

    expect(executed1).toBe(true)
    expect(executed2).toBe(true)
    expect(executed3).toBe(true)
  })
})
describe('test GroupTaskQueue with different ids', () => {
  let timer

  beforeAll(() => {
    timer = { currentTime: 0, timerInterval: null }
    startTimer(timer)
  })

  afterAll(() => {
    stopTimer(timer)
  })
  test('test GroupTaskQueue with different ids', async () => {
    let executed1 = false
    let executed2 = false
    let executed3 = false

    const queue = new GroupTaskQueue()
    queue.add(async () => {
      await sleep(timer, 20)
      executed1 = true
    }, 1)

    await sleep(timer, 10)

    expect(executed1).toBe(false)
    expect(executed2).toBe(false)
    expect(executed3).toBe(false)

    queue.add(async () => {
      await sleep(timer, 20)
      executed2 = true
    }, 2)
    queue.add(async () => {
      await sleep(timer, 30)
      executed3 = true
    }, 1)

    await sleep(timer, 30)

    expect(executed1).toBe(true)
    expect(executed2).toBe(true)
    expect(executed3).toBe(false)

    await sleep(timer, 10)

    expect(executed1).toBe(true)
    expect(executed2).toBe(true)
    expect(executed3).toBe(true)
  })
})
describe('test GroupTaskQueue with waiting for add to resolve', () => {
  let timer

  beforeAll(() => {
    timer = { currentTime: 0, timerInterval: null }
    startTimer(timer)
  })

  afterAll(() => {
    stopTimer(timer)
  })
  test('test GroupTaskQueue with waiting for add to resolve', async () => {
    let executed1 = false
    let executed2 = false
    let executed3 = false

    const queue = new GroupTaskQueue()
    queue
      .add(async () => {
        await sleep(timer, 20)
      })
      .then(() => {
        executed1 = true
      })
    queue
      .add(async () => {
        await sleep(timer, 20)
      })
      .then(() => {
        executed2 = true
      })
    queue
      .add(async () => {
        await sleep(timer, 20)
      })
      .then(() => {
        executed3 = true
      })

    await sleep(timer, 50)

    expect(executed1).toBe(true)
    expect(executed2).toBe(true)
    expect(executed3).toBe(false)
  })
})
describe('test GroupTaskQueue with exception during execution', () => {
  let timer

  beforeAll(() => {
    timer = { currentTime: 0, timerInterval: null }
    startTimer(timer)
  })

  afterAll(() => {
    stopTimer(timer)
  })
  test('test GroupTaskQueue with exception during execution', async () => {
    let failed1 = false
    let failed1Error = null
    let failed2 = false

    const queue = new GroupTaskQueue()
    queue
      .add(async () => {
        await sleep(timer, 20)
        throw new Error('test')
      })
      .then(() => {
        failed1 = false
      })
      .catch((error) => {
        failed1Error = error
        failed1 = true
      })
    queue
      .add(async () => {
        await sleep(timer, 20)
      })
      .then(() => {
        failed2 = false
      })
      .catch(() => {
        failed2 = true
      })

    await sleep(timer, 50)

    expect(failed1).toBe(true)
    expect(failed1Error.toString()).toBe('Error: test')
    expect(failed2).toBe(false)
  })
})
describe('test GroupTaskQueue with lock', () => {
  let timer

  beforeAll(() => {
    timer = { currentTime: 0, timerInterval: null }
    startTimer(timer)
  })

  afterAll(() => {
    stopTimer(timer)
  })
  test('test GroupTaskQueue with exception during execution', async () => {
    let executed1 = false
    let executed2 = false
    let executed3 = false

    const queue = new GroupTaskQueue()
    queue.lock(1)
    queue.lock(2)

    queue.add(async () => {
      await sleep(timer, 20)
      executed1 = true
    }, 1)
    queue.add(async () => {
      await sleep(timer, 20)
      executed2 = true
    }, 2)
    queue.add(async () => {
      await sleep(timer, 20)
      executed3 = true
    }, 1)

    await sleep(timer, 30)

    expect(executed1).toBe(false)
    expect(executed2).toBe(false)
    expect(executed3).toBe(false)

    queue.release(2)

    await sleep(timer, 30)

    expect(executed1).toBe(false)
    expect(executed2).toBe(true)
    expect(executed3).toBe(false)

    queue.release(1)

    await sleep(timer, 30)

    expect(executed1).toBe(true)
    expect(executed2).toBe(true)
    expect(executed3).toBe(false)

    await sleep(timer, 20)

    expect(executed1).toBe(true)
    expect(executed2).toBe(true)
    expect(executed3).toBe(true)
  })
})
describe('test queue deleted from GroupTaskQueue', () => {
  let timer

  beforeAll(() => {
    timer = { currentTime: 0, timerInterval: null }
    startTimer(timer)
  })

  afterAll(() => {
    stopTimer(timer)
  })
  test('test queue deleted from GroupTaskQueue', async () => {
    const queue = new GroupTaskQueue()
    queue.add(async () => {
      await sleep(timer, 20)
    }, 1)

    expect(Object.prototype.hasOwnProperty.call(queue.queues, 1)).toBe(true)

    await sleep(timer, 30)

    expect(Object.prototype.hasOwnProperty.call(queue.queues, 1)).toBe(false)
  })
})
