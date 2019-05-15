def element_for(root, ent_seq):
    return root.xpath('//entry/ent_seq[.="' + ent_seq + '"]/..')[0]
