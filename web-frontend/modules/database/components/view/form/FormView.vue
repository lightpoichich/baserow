<template>
  <div class="form-view">
    <div class="form-view__sidebar">
      <div class="form-view__fields">
        <div class="form-view__fields-head">
          <div class="form-view__fields-title">Fields</div>
          <ul class="form-view__fields-actions">
            <li>
              <a href="#">add all</a>
            </li>
            <li>
              <a href="#">remove all</a>
            </li>
          </ul>
        </div>
        <p class="form-view__fields-description">
          All the fields are in the form.
        </p>
        <div class="form-view__fields-list">
          <a href="#" class="form-view__fields-item">
            <i class="form-view__fields-icon fas fa-hashtag"></i>
            <div class="form-view__fields-name">Price</div>
          </a>
          <a href="#" class="form-view__fields-item">
            <i class="form-view__fields-icon fas fa-hashtag"></i>
            <div class="form-view__fields-name">Price</div>
          </a>
          <a href="#" class="form-view__fields-item">
            <i class="form-view__fields-icon fas fa-hashtag"></i>
            <div class="form-view__fields-name">
              Price with a very long name that does not fit anymore
            </div>
          </a>
        </div>
        <div class="form-view__fields-create">
          <a href="#">
            <i class="fas fa-plus"></i>
            Create new field
          </a>
        </div>
      </div>
    </div>
    <div class="form-view__preview">
      <div class="form-view__page form-view__page--rounded">
        <div class="form-view__cover">
          <a class="form-view__file">Add a cover image</a>
        </div>
        <div class="form-view__body">
          <div class="form-view__heading">
            <a class="form-view__file">Add a logo</a>
            <h1 class="form-view__title">
              Custom title
              <a href="#" class="form-view__edit"></a>
            </h1>
            <p class="form-view__description">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
              gravida, tellus vel finibus blandit, urna ligula egestas nisi, in
              hendrerit nibh purus porta velit. Praesent id
              <a href="#" class="form-view__edit"></a>
            </p>
          </div>
          <div
            class="form-view__field form-view__field--editable form-view__field--selected"
          >
            <div class="form-view__field-head">
              <div class="form-view__field-head-icon">
                <i class="fas fa-fw fa-hashtag"></i>
              </div>
              <div class="form-view__field-head-name">Full name of field</div>
              <a href="#" class="form-view__field-head-options">
                <i class="fas fa-caret-down"></i>
              </a>
              <a href="#" class="form-view__field-head-hide">
                <i class="fas fa-eye-slash"></i>
              </a>
            </div>
            <div class="form-view__field-inner">
              <div class="form-view__field-name">
                Custom name
                <a href="#" class="form-view__edit"></a>
              </div>
              <div class="form-view__field-description">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
                gravida, tellus vel.
                <a href="#" class="form-view__edit"></a>
              </div>
              <div class="form-view__field-control">
                <input
                  type="text"
                  name=""
                  value=""
                  class="input input--large"
                />
              </div>
              <div class="form-view__field-options">
                <SwitchInput v-model="required" :large="true"
                  >required</SwitchInput
                >
              </div>
            </div>
          </div>
          <div class="form-view__field form-view__field--editable">
            <div class="form-view__field-head">
              <div class="form-view__field-head-icon">
                <i class="fas fa-fw fa-hashtag"></i>
              </div>
              <div class="form-view__field-head-name">Full name of field</div>
              <a href="#" class="form-view__field-head-options">
                <i class="fas fa-caret-down"></i>
              </a>
              <a href="#" class="form-view__field-head-hide">
                <i class="fas fa-eye-slash"></i>
              </a>
            </div>
            <div class="form-view__field-inner">
              <div class="form-view__field-name">Custom name</div>
              <div class="form-view__field-description">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
                gravida, tellus vel.
              </div>
              <div class="form-view__field-control">
                <input
                  type="text"
                  name=""
                  value=""
                  class="input input--large"
                />
              </div>
              <div class="form-view__field-options">
                <SwitchInput v-model="required" :large="true"
                  >required</SwitchInput
                >
              </div>
            </div>
          </div>
          <div class="form-view__actions">
            <div class="form-view__powered-by">
              Powered by
              <a href="https://baserow.io" target="_blank">
                <img
                  class="form-view__powered-by-logo"
                  src="@baserow/modules/core/static/img/logo.svg"
                  alt=""
                />
              </a>
            </div>
            <div class="form-view__submit">
              <a href="#" class="button button--primary button--large"
                >Submit</a
              >
            </div>
          </div>
        </div>
        <div class="form-view__meta">
          <div class="form-view__body">
            <div class="form-view__meta-controls">
              <div class="control">
                <label class="control__label">When the form is submitted</label>
                <div class="control__elements">
                  <ul class="choice-items choice-items--inline">
                    <li>
                      <a class="choice-items__link active">Show a message</a>
                    </li>
                    <li>
                      <a class="choice-items__link">Redirect to URL</a>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="control">
                <label class="control__label">The URL</label>
                <div class="control__elements">
                  <input
                    ref="name"
                    type="text"
                    class="input"
                    placeholder="The URL"
                  />
                </div>
              </div>
              <div class="control">
                <div class="control__elements">
                  <SwitchInput v-model="required" :large="true"
                    >Sent an email to</SwitchInput
                  >
                  <div class="form-view__meta-email">
                    <input
                      ref="name"
                      type="text"
                      class="input"
                      placeholder="The URL"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FormView',
  data() {
    return {
      required: true,
    }
  },
}
</script>
