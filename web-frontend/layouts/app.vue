<template>
  <div :class="{ 'layout-collapsed': isCollapsed }" class="layout">
    <div class="layout-col-1 menu">
      <ul class="menu-items">
        <li class="menu-item">
          <nuxt-link :to="{ name: 'app' }" class="menu-link">
            <i class="fas fa-tachometer-alt"></i>
            <span class="menu-link-text">Dashboard</span>
          </nuxt-link>
        </li>
        <li class="menu-item">
          <a href="#" class="menu-link" data-context=".select">
            <i class="fas fa-layer-group"></i>
            <span class="menu-link-text">Groups</span>
          </a>
          <div class="select hidden">
            <div class="select-search">
              <i class="select-search-icon fas fa-search"></i>
              <input
                type="text"
                class="select-search-input"
                placeholder="Search views"
              />
            </div>
            <ul class="select-items">
              <li class="select-item active">
                <a href="#" class="select-item-link">Group name 1</a>
                <a href="#" class="select-item-options" data-context=".context">
                  <i class="fas fa-ellipsis-v"></i>
                </a>
                <div class="context hidden">
                  <ul class="context-menu">
                    <li>
                      <a href="#">
                        <i class="context-menu-icon fas fa-fw fa-pen"></i>
                        Rename group
                      </a>
                    </li>
                    <li>
                      <a href="#">
                        <i class="context-menu-icon fas fa-fw fa-trash"></i>
                        Delete group
                      </a>
                    </li>
                  </ul>
                </div>
              </li>
              <li class="select-item">
                <a href="#" class="select-item-link">Group name 2</a>
                <a href="#" class="select-item-options">
                  <i class="fas fa-ellipsis-v"></i>
                </a>
              </li>
              <li class="select-item">
                <a href="#" class="select-item-link">Group name 3</a>
                <a href="#" class="select-item-options">
                  <i class="fas fa-ellipsis-v"></i>
                </a>
              </li>
              <li class="select-item">
                <a href="#" class="select-item-link">Group name 4</a>
                <a href="#" class="select-item-options">
                  <i class="fas fa-ellipsis-v"></i>
                </a>
              </li>
            </ul>
            <div class="select-footer">
              <a href="#" class="select-footer-button">
                <i class="fas fa-plus"></i>
                Do something
              </a>
            </div>
          </div>
        </li>
      </ul>
      <ul class="menu-items">
        <li class="menu-item layout-uncollapse">
          <a class="menu-link" @click="toggleCollapsed()">
            <i class="menu-item-icon fas fa-angle-double-right"></i>
            <span class="menu-link-text">Uncollapse</span>
          </a>
        </li>
        <li class="menu-item">
          <a
            class="menu-link menu-user-item"
            @click="$refs.userContext.toggle($event.target)"
          >
            {{ nameAbbreviation }}
            <span class="menu-link-text">{{ name }}</span>
          </a>
          <Context ref="userContext">
            <div class="context-menu-title">{{ name }}</div>
            <ul class="context-menu">
              <li>
                <a @click="logoff()">
                  <i class="context-menu-icon fas fa-fw fa-sign-out-alt"></i>
                  Logoff
                </a>
              </li>
            </ul>
          </Context>
        </li>
      </ul>
    </div>
    <div class="layout-col-2 sidebar">
      <div class="sidebar-content-wrapper">
        <nav class="sidebar-content">
          <div class="sidebar-title">
            <img src="@/static/img/logo.svg" alt="" />
          </div>
          <div class="sidebar-group-title">Group name 1</div>
          <ul class="tree">
            <li class="tree-item">
              <div class="tree-action">
                <a href="#" class="tree-link">
                  <i class="tree-type fas fa-database"></i>
                  Vehicles
                </a>
                <a href="#" class="tree-options" data-context=".context">
                  <i class="fas fa-ellipsis-v"></i>
                </a>
                <div class="context hidden">
                  <div class="context-menu-title">Vehicles</div>
                  <ul class="context-menu">
                    <li>
                      <a href="#">
                        <i class="context-menu-icon fas fa-fw fa-pen"></i>
                        Rename database
                      </a>
                    </li>
                    <li>
                      <a href="#">
                        <i class="context-menu-icon fas fa-fw fa-trash"></i>
                        Delete table
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </li>
            <li class="tree-item">
              <div class="tree-action">
                <a href="#" class="tree-link">
                  <i class="tree-type fas fa-angle-right"></i>
                  Map nummer 1
                </a>
              </div>
            </li>
            <li class="tree-item active">
              <div class="tree-action">
                <a href="#" class="tree-link">
                  <i class="tree-type fas fa-database"></i>
                  Webshop
                </a>
                <a href="#" class="tree-options">
                  <i class="fas fa-ellipsis-v"></i>
                </a>
              </div>
              <ul class="tree-subs">
                <li class="tree-sub active">
                  <a href="#" class="tree-sub-link">Customers</a>
                  <a href="#" class="tree-options">
                    <i class="fas fa-ellipsis-v"></i>
                  </a>
                </li>
                <li class="tree-sub">
                  <a href="#" class="tree-sub-link">Products very long name</a>
                  <a href="#" class="tree-options">
                    <i class="fas fa-ellipsis-v"></i>
                  </a>
                </li>
                <li class="tree-sub">
                  <a href="#" class="tree-sub-link">Categories</a>
                  <a href="#" class="tree-options">
                    <i class="fas fa-ellipsis-v"></i>
                  </a>
                </li>
              </ul>
            </li>
            <li class="tree-item">
              <div class="tree-action">
                <a href="#" class="tree-link">
                  <i class="tree-type fas fa-angle-down"></i>
                  Map nummer 1
                </a>
              </div>
              <ul class="tree">
                <li class="tree-item">
                  <div class="tree-action">
                    <a href="#" class="tree-link">
                      <i class="tree-type fas fa-database"></i>
                      Vehicles
                    </a>
                    <a href="#" class="tree-options">
                      <i class="fas fa-ellipsis-v"></i>
                    </a>
                  </div>
                </li>
                <li class="tree-item">
                  <div class="tree-action">
                    <a href="#" class="tree-link">
                      <i class="tree-type fas fa-database"></i>
                      Something
                    </a>
                    <a href="#" class="tree-options">
                      <i class="fas fa-ellipsis-v"></i>
                    </a>
                  </div>
                </li>
              </ul>
            </li>
            <li class="tree-item">
              <div class="tree-action">
                <a href="#" class="tree-link">
                  <i class="tree-type fas fa-database"></i>
                  Vehicles with very long name and that is not good.
                </a>
                <a href="#" class="tree-options">
                  <i class="fas fa-ellipsis-v"></i>
                </a>
              </div>
            </li>
            <li class="tree-item">
              <div class="tree-action">
                <a href="#" class="tree-link">
                  <i class="tree-type fas fa-database"></i>
                  Something else
                </a>
                <a href="#" class="tree-options">
                  <i class="fas fa-ellipsis-v"></i>
                </a>
              </div>
            </li>
          </ul>
        </nav>
      </div>
      <div class="sidebar-footer">
        <a class="sidebar-collapse" @click="toggleCollapsed()">
          <i class="fas fa-angle-double-left"></i>
          Collapse sidebar
        </a>
      </div>
    </div>
    <div class="layout-col-3">
      <nuxt />
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

import Context from '@/components/Context'

export default {
  layout: 'default',
  middleware: 'authenticated',
  components: {
    Context
  },
  computed: {
    ...mapGetters({
      isCollapsed: 'sidebar/isCollapsed',
      name: 'auth/getName',
      nameAbbreviation: 'auth/getNameAbbreviation'
    })
  },
  methods: {
    logoff() {
      this.$store.dispatch('auth/logoff')
      this.$nuxt.$router.replace({ name: 'login' })
    },
    ...mapActions({
      toggleCollapsed: 'sidebar/toggleCollapsed'
    })
  }
}
</script>
