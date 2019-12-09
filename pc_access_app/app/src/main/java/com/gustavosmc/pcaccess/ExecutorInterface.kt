package com.gustavosmc.pcaccess

interface ExecutorInterface {
    fun connect()
    fun disconnect()

    fun turn_on_mouse(port: Int)
    fun turn_off_mouse()
}