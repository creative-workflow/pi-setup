module PublisherModelMixin
  #static per model
  publisher_context_model = nil

  #called when a page publish starts
  def self.on_page_publish_start page_id
    publisher_context_model = PagePublishContextModel.new page_id
  end

  after_initialize: update_publisher_context

  def update_publisher_context
    publisher_context_model.register_context get_publish_context, updated_at
  end

  def get_publish_context
    self.ancestors.first.dasherize+'-id-'+id
  end
end


class PagePublishContextModel
  PAGES_PER_CONTEXT = {} #should be a shared ressource, mongo for ex.
  INVALID_CONTEXTS  = [] # "-"

  def initialize page_id, publish_start
    @page_id = page_id
    @publish_start = publish_start
  end

  def register_context context_key, context_updated_at
    if not PAGES_PER_CONTEXT.has_key? context_key
      PAGES_PER_CONTEXT[context_key] = []
    end

    #remember which contexts a page is memeber
    PAGES_PER_CONTEXT[context_key] << @page_id

    #mark invalid contexts
    if context_updated_at > @publish_start
       INVALID_CONTEXTS << @page_id
    end
  end

  def invalid_pages
    #filter invalid pages by context
    PAGES_PER_CONTEXT.select_values do |context_key, page_ids|
      INVALID_CONTEXTS.include? context_key
    end.flatten.uniq
  end
end

